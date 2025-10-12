from datetime import date, datetime, timedelta

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.appointment import appointment_crud
from app.crud.professional import professional_crud
from app.models.enums import AppointmentStatus, ProfessionalCategory
from app.models.professional import ProfessionalProfile, ProfileTag, UnavailableDate
from app.schemas.professional import (
    AvailableSlotsResponse,
    ProfessionalProfileCreate,
    ProfessionalProfileResponse,
    ProfessionalProfileUpdate,
    TimeSlot,
)
from app.utils.exceptions import (
    BadRequestException,
    ForbiddenException,
    NotFoundException,
)


async def create_professional_profile(
    db: AsyncSession,
    user_id: int,
    profissional_identification: str,
    category: str,
) -> ProfessionalProfile:
    existing = await professional_crud.get_by_user_id(db, user_id=user_id)
    if existing:
        raise BadRequestException("Professional profile already exists")

    existing_id = await professional_crud.get_by_identification(
        db, identification=profissional_identification
    )
    if existing_id:
        raise BadRequestException("Professional identification already in use")

    profile = ProfessionalProfile(
        user_id=user_id,
        profissional_identification=profissional_identification,
        category=ProfessionalCategory(category),
    )
    db.add(profile)
    await db.flush()
    return profile


async def create_full_professional_profile(
    db: AsyncSession, user_id: int, profile_in: ProfessionalProfileCreate
) -> ProfessionalProfile:
    existing = await professional_crud.get_by_user_id(db, user_id=user_id)
    if existing:
        raise BadRequestException("Professional profile already exists")

    existing_id = await professional_crud.get_by_identification(
        db, identification=profile_in.profissional_identification
    )
    if existing_id:
        raise BadRequestException("Professional identification already in use")

    profile_data = profile_in.model_dump(exclude={"tags", "unavailable_dates"})
    profile = ProfessionalProfile(**profile_data, user_id=user_id)
    db.add(profile)
    await db.flush()

    if profile_in.tags:
        for tag_name in profile_in.tags:
            tag = ProfileTag(profile_id=profile.id, name=tag_name)
            db.add(tag)

    if profile_in.unavailable_dates:
        for date_in in profile_in.unavailable_dates:
            unavailable = UnavailableDate(
                profile_id=profile.id,
                date=date_in.date,
                reason=date_in.reason,
            )
            db.add(unavailable)

    await db.commit()
    await db.refresh(profile)
    return profile


async def get_professional_profile(
    db: AsyncSession, profile_id: int
) -> ProfessionalProfile:
    profile = await professional_crud.get_with_relations(db, id=profile_id)
    if not profile:
        raise NotFoundException("Professional profile not found")
    return profile


async def get_professional_profile_by_user(
    db: AsyncSession, user_id: int
) -> ProfessionalProfile:
    profile = await professional_crud.get_by_user_id(db, user_id=user_id)
    if not profile:
        raise NotFoundException("Professional profile not found")
    return profile


async def update_professional_profile(
    db: AsyncSession,
    user_id: int,
    profile_id: int,
    profile_in: ProfessionalProfileUpdate,
) -> ProfessionalProfile:
    profile = await get_professional_profile(db, profile_id)

    if profile.user_id != user_id:
        raise ForbiddenException("Not authorized to update this profile")

    update_data = profile_in.model_dump(
        exclude={"tags", "unavailable_dates"}, exclude_unset=True
    )
    for field, value in update_data.items():
        setattr(profile, field, value)

    if profile_in.tags is not None:
        try:
            delete(ProfileTag).where(ProfileTag.profile_id == profile.id)
        except Exception as e:
            BadRequestException(f"Error deleting tags: {e}")

        for tag_name in profile_in.tags:
            tag = ProfileTag(profile_id=profile.id, name=tag_name)
            db.add(tag)

    if profile_in.unavailable_dates is not None:
        try:
            delete(UnavailableDate).where(UnavailableDate.profile_id == profile.id)
        except Exception as e:
            BadRequestException(f"Error deleting unavailable dates: {e}")

        for date_in in profile_in.unavailable_dates:
            unavailable = UnavailableDate(
                profile_id=profile.id,
                date=date_in.date,
                reason=date_in.reason,
            )
            db.add(unavailable)

    await db.commit()
    await db.refresh(profile)
    return profile


async def delete_professional_profile(
    db: AsyncSession, user_id: int, profile_id: int
) -> None:
    profile = await get_professional_profile(db, profile_id)

    if profile.user_id != user_id:
        raise ForbiddenException("Not authorized to delete this profile")

    await professional_crud.delete(db, pk=profile.id)
    await db.commit()


async def list_professionals(
    db: AsyncSession,
    category: str | None = None,
    name: str | None = None,
    tags: list[str] | None = None,
    only_online: bool | None = None,
    only_presential: bool | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[ProfessionalProfileResponse]:
    profiles = await professional_crud.list_professionals(
        db,
        category=category,
        name=name,
        tags=tags,
        only_online=only_online,
        only_presential=only_presential,
        skip=skip,
        limit=limit,
    )

    responses = []
    for profile in profiles:
        response = ProfessionalProfileResponse(
            id=profile.id,
            user_id=profile.user_id,
            bio=profile.bio,
            category=profile.category,
            profissional_identification=profile.profissional_identification,
            services=profile.services,
            price=profile.price,
            only_online=profile.only_online,
            only_presential=profile.only_presential,
            rating=profile.rating,
            num_reviews=profile.num_reviews,
            available_days_of_week=profile.available_days_of_week,
            start_hour=profile.start_hour,
            end_hour=profile.end_hour,
            user_name=profile.user.name if profile.user else None,
            email=profile.user.email if profile.user else None,
            phone=profile.user.phone if profile.user else None,
            cep=profile.user.cep if profile.user else None,
            uf=profile.user.uf if profile.user else None,
            city=profile.user.city if profile.user else None,
            address=profile.user.address if profile.user else None,
            tags=[tag.name for tag in profile.tags],
            unavailable_dates=[],
        )
        responses.append(response)

    return responses


async def get_available_slots(
    db: AsyncSession, profile_id: int, target_date: date, duration_minutes: int
) -> AvailableSlotsResponse:
    """Calcular horários disponíveis de um profissional para uma data específica."""
    profile = await get_professional_profile(db, profile_id)

    # Verificar se o profissional tem horários configurados
    if not profile.start_hour or not profile.end_hour:
        return AvailableSlotsResponse(
            date=target_date,
            available_slots=[],
            unavailable_reason="Profissional não configurou horários de atendimento",
        )

    # Verificar dia da semana
    weekday_map = {
        0: "monday",
        1: "tuesday",
        2: "wednesday",
        3: "thursday",
        4: "friday",
        5: "saturday",
        6: "sunday",
    }
    weekday = weekday_map[target_date.weekday()]

    available_days = (profile.available_days_of_week or "").split(",")
    available_days = [d.strip().lower() for d in available_days if d.strip()]

    if available_days and weekday not in available_days:
        return AvailableSlotsResponse(
            date=target_date,
            available_slots=[],
            unavailable_reason=f"Profissional não atende às {weekday}s",
        )

    # Verificar datas indisponíveis
    unavailable_result = await db.execute(
        select(UnavailableDate).where(
            UnavailableDate.profile_id == profile_id,
            UnavailableDate.date == str(target_date),
        )
    )
    if unavailable_result.scalar_one_or_none():
        return AvailableSlotsResponse(
            date=target_date,
            available_slots=[],
            unavailable_reason="Data marcada como indisponível",
        )

    # Buscar agendamentos do dia
    appointments = await appointment_crud.get_by_professional_and_date(
        db, professional_id=profile_id, start_date=target_date, end_date=target_date
    )

    # Filtrar apenas agendamentos não cancelados
    booked_slots = [
        (apt.start_time.time(), apt.end_time.time())
        for apt in appointments
        if apt.status != AppointmentStatus.CANCELLED
    ]

    # Gerar slots disponíveis
    start_hour, start_minute = map(int, profile.start_hour.split(":"))
    end_hour, end_minute = map(int, profile.end_hour.split(":"))

    current_time = datetime.combine(target_date, datetime.min.time()).replace(
        hour=start_hour, minute=start_minute
    )
    end_time = datetime.combine(target_date, datetime.min.time()).replace(
        hour=end_hour, minute=end_minute
    )

    available_slots = []

    while current_time + timedelta(minutes=duration_minutes) <= end_time:
        slot_start = current_time.time()
        slot_end = (current_time + timedelta(minutes=duration_minutes)).time()

        # Verificar se o slot está livre
        is_available = True
        for booked_start, booked_end in booked_slots:
            if not (slot_end <= booked_start or slot_start >= booked_end):
                is_available = False
                break

        if is_available:
            available_slots.append(
                TimeSlot(
                    start_time=slot_start.strftime("%H:%M"),
                    end_time=slot_end.strftime("%H:%M"),
                )
            )

        current_time += timedelta(minutes=duration_minutes)

    return AvailableSlotsResponse(date=target_date, available_slots=available_slots)


async def build_professional_response_with_reviews(
    profile: ProfessionalProfile,
    limit_reviews: int = 5,
) -> dict:
    """
    Constrói resposta do profissional incluindo reviews recentes.
    """
    from app.schemas.professional import ReviewSummary

    # Pegar as últimas N reviews
    recent_reviews = sorted(
        profile.reviews, key=lambda r: r.created_at, reverse=True
    )[:limit_reviews]

    reviews_data = []
    for review in recent_reviews:
        patient_name = None
        if not review.is_anonymous and review.patient:
            patient_name = review.patient.name

        reviews_data.append(
            ReviewSummary(
                id=review.id,
                rating=review.rating,
                comment=review.comment,
                patient_name=patient_name,
                is_anonymous=review.is_anonymous,
                created_at=review.created_at.isoformat(),
            )
        )

    return {
        "id": profile.id,
        "user_id": profile.user_id,
        "bio": profile.bio,
        "category": profile.category,
        "profissional_identification": profile.profissional_identification,
        "services": profile.services,
        "price": profile.price,
        "only_online": profile.only_online,
        "only_presential": profile.only_presential,
        "rating": profile.rating,
        "num_reviews": profile.num_reviews,
        "available_days_of_week": profile.available_days_of_week,
        "start_hour": profile.start_hour,
        "end_hour": profile.end_hour,
        "user_name": profile.user.name if profile.user else None,
        "email": profile.user.email if profile.user else None,
        "phone": profile.user.phone if profile.user else None,
        "cep": profile.user.cep if profile.user else None,
        "uf": profile.user.uf if profile.user else None,
        "city": profile.user.city if profile.user else None,
        "address": profile.user.address if profile.user else None,
        "tags": [tag.name for tag in profile.tags],
        "unavailable_dates": [],
        "reviews": reviews_data,
    }
