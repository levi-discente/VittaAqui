package repositories

import (
	"time"

	"github.com/levirenato/VittaAqui/internal/models"
	"gorm.io/gorm"
)

type AppointmentRepository struct {
	db *gorm.DB
}

func NewAppointmentRepository(db *gorm.DB) *AppointmentRepository {
	return &AppointmentRepository{db}
}

func (r *AppointmentRepository) FindCancelled(patientID, professionalID uint, start, end time.Time) (*models.Appointment, error) {
	var ap models.Appointment
	err := r.db.
		Where("patient_id = ? AND professional_id = ? AND status = ?", patientID, professionalID, "cancelled").
		Where("start_time = ? AND end_time = ?", start, end).
		First(&ap).Error
	if err != nil {
		return nil, err
	}
	return &ap, nil
}

func (r *AppointmentRepository) Create(appointment *models.Appointment) error {
	return r.db.Create(appointment).Error
}

func (r *AppointmentRepository) ListByProfessional(professionalID uint) ([]models.Appointment, error) {
	var appointments []models.Appointment
	err := r.db.Where("professional_id = ?", professionalID).Find(&appointments).Error
	return appointments, err
}

func (r *AppointmentRepository) ListByPatient(patientID uint) ([]models.Appointment, error) {
	var appointments []models.Appointment
	err := r.db.Where("patient_id = ?", patientID).Find(&appointments).Error
	return appointments, err
}

func (r *AppointmentRepository) FindConflicts(professionalID uint, start, end time.Time) ([]models.Appointment, error) {
	var conflicts []models.Appointment

	err := r.db.
		Where("professional_id = ?", professionalID).
		Where("start_time < ? AND end_time > ?", end, start).
		Where("status != ?", "cancelled").
		Find(&conflicts).Error

	return conflicts, err
}

func (r *AppointmentRepository) FindByID(id uint) (*models.Appointment, error) {
	var ap models.Appointment
	err := r.db.Preload("Patient").Preload("Professional.User").First(&ap, id).Error
	return &ap, err
}

func (r *AppointmentRepository) Update(id uint, start, end time.Time, status string) error {
	return r.db.Model(&models.Appointment{}).
		Where("id = ?", id).
		Updates(map[string]interface{}{
			"start_time": start,
			"end_time":   end,
			"status":     status,
		}).Error
}

func (r *AppointmentRepository) Delete(id uint) error {
	return r.db.Delete(&models.Appointment{}, id).Error
}

func (r *AppointmentRepository) ListScheduleWithDetails(professionalID uint) ([]models.Appointment, error) {
	var appointments []models.Appointment
	err := r.db.
		Where("professional_id = ?", professionalID).
		Preload("Patient").
		Find(&appointments).Error
	return appointments, err
}

func (r *AppointmentRepository) ListPatientAppointmentsWithProfessional(patientID uint) ([]models.Appointment, error) {
	var appointments []models.Appointment
	err := r.db.
		Where("patient_id = ?", patientID).
		Preload("Professional.User").
		Find(&appointments).Error
	return appointments, err
}
