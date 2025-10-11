"""Professional profile service."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.professional import professional_crud
from app.models.enums import ProfessionalCategory
from app.models.professional import ProfessionalProfile, ProfileTag, UnavailableDate
from app.schemas.professional import (
    ProfessionalProfileCreate,
    ProfessionalProfileResponse,
    ProfessionalProfileUpdate,
)
from app.utils.exceptions import BadRequestException, ForbiddenException, NotFoundException


async def create_professional_profile(
    db: AsyncSession,
    user_id: int,
    profissional_identification: str,
    category: str,
) -> ProfessionalProfile:
    """Create a basic professional profile (called during user registration)."""
    # Check if profile already exists
    existing = await professional_crud.get_by_user_id(db, user_id=user_id)
    if existing:
        raise BadRequestException("Professional profile already exists")

    # Check if identification already exists
    existing_id = await professional_crud.get_by_identification(
        db, identification=profissional_identification
    )
    if existing_id:
        raise BadRequestException("Professional identification already in use")

    # Create profile
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
    """Create a complete professional profile with all details."""
    # Check if profile already exists
    existing = await professional_crud.get_by_user_id(db, user_id=user_id)
    if existing:
        raise BadRequestException("Professional profile already exists")

    # Check if identification already exists
    existing_id = await professional_crud.get_by_identification(
        db, identification=profile_in.profissional_identification
    )
    if existing_id:
        raise BadRequestException("Professional identification already in use")

    # Create profile
    profile_data = profile_in.model_dump(exclude={"tags", "unavailable_dates"})
    profile = ProfessionalProfile(**profile_data, user_id=user_id)
    db.add(profile)
    await db.flush()

    # Add tags
    if profile_in.tags:
        for tag_name in profile_in.tags:
            tag = ProfileTag(profile_id=profile.id, name=tag_name)
            db.add(tag)

    # Add unavailable dates
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


async def get_professional_profile(db: AsyncSession, profile_id: int) -> ProfessionalProfile:
    """Get professional profile by ID."""
    profile = await professional_crud.get_with_relations(db, id=profile_id)
    if not profile:
        raise NotFoundException("Professional profile not found")
    return profile


async def get_professional_profile_by_user(
    db: AsyncSession, user_id: int
) -> ProfessionalProfile:
    """Get professional profile by user ID."""
    profile = await professional_crud.get_by_user_id(db, user_id=user_id)
    if not profile:
        raise NotFoundException("Professional profile not found")
    return profile


async def update_professional_profile(
    db: AsyncSession, user_id: int, profile_id: int, profile_in: ProfessionalProfileUpdate
) -> ProfessionalProfile:
    """Update professional profile."""
    profile = await get_professional_profile(db, profile_id)

    # Check ownership
    if profile.user_id != user_id:
        raise ForbiddenException("Not authorized to update this profile")

    # Update basic fields
    update_data = profile_in.model_dump(
        exclude={"tags", "unavailable_dates"}, exclude_unset=True
    )
    for field, value in update_data.items():
        setattr(profile, field, value)

    # Update tags if provided
    if profile_in.tags is not None:
        # Remove old tags
        await db.execute(
            ProfileTag.__table__.delete().where(ProfileTag.profile_id == profile.id)
        )
        # Add new tags
        for tag_name in profile_in.tags:
            tag = ProfileTag(profile_id=profile.id, name=tag_name)
            db.add(tag)

    # Update unavailable dates if provided
    if profile_in.unavailable_dates is not None:
        # Remove old dates
        await db.execute(
            UnavailableDate.__table__.delete().where(
                UnavailableDate.profile_id == profile.id
            )
        )
        # Add new dates
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
    """Delete professional profile."""
    profile = await get_professional_profile(db, profile_id)

    # Check ownership
    if profile.user_id != user_id:
        raise ForbiddenException("Not authorized to delete this profile")

    await professional_crud.delete(db, id=profile.id)
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
    """List professional profiles with filters."""
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

    # Convert to response schema
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
