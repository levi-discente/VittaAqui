package services

import (
	"errors"
	"time"

	"github.com/levirenato/VittaAqui/internal/models"
	"github.com/levirenato/VittaAqui/internal/repositories"
)

var ErrTimeConflict = errors.New("there is a scheduling conflict for this time slot")

type AppointmentService struct {
	repo *repositories.AppointmentRepository
}

func NewAppointmentService(repo *repositories.AppointmentRepository) *AppointmentService {
	return &AppointmentService{repo}
}

func (s *AppointmentService) CreateAppointment(patientID, professionalID uint, start, end time.Time) error {
	// 1. Verifica conflitos de horário
	conflicts, err := s.repo.FindConflicts(professionalID, start, end)
	if err != nil {
		return err
	}
	if len(conflicts) > 0 {
		return ErrTimeConflict
	}

	// 2. Cria agendamento
	ap := &models.Appointment{
		PatientID:      patientID,
		ProfessionalID: professionalID,
		StartTime:      start,
		EndTime:        end,
		Status:         "pending",
	}
	return s.repo.Create(ap)
}

func (s *AppointmentService) UpdateAppointment(appointmentID uint, start, end time.Time, status string) error {
	ap, err := s.repo.FindByID(appointmentID)
	if err != nil {
		return err
	}

	conflicts, err := s.repo.FindConflicts(ap.ProfessionalID, start, end)
	if err != nil {
		return err
	}
	for _, c := range conflicts {
		if c.ID != ap.ID {
			return ErrTimeConflict
		}
	}

	ap.StartTime = start
	ap.EndTime = end
	ap.Status = status
	return s.repo.Update(ap.ID, ap.StartTime, ap.EndTime, ap.Status)
}

func (s *AppointmentService) GetSchedule(professionalID uint) ([]models.Appointment, error) {
	return s.repo.ListScheduleWithDetails(professionalID)
}

func (s *AppointmentService) GetPatientAppointments(patientID uint) ([]models.Appointment, error) {
	return s.repo.ListPatientAppointmentsWithProfessional(patientID)
}

func (s *AppointmentService) GetAppointmentsByPatient(patientID uint) ([]models.Appointment, error) {
	return s.repo.ListByPatient(patientID)
}

func (s *AppointmentService) GetAppointmentsByProfessional(professionalID uint) ([]models.Appointment, error) {
	return s.repo.ListByProfessional(professionalID)
}

func (s *AppointmentService) DeleteAppointment(appointmentID uint) error {
	return s.repo.Delete(appointmentID)
}
