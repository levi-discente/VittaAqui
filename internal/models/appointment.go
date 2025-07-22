package models

import "time"

type Appointment struct {
	ID             uint                `gorm:"primaryKey" json:"id"`
	PatientID      uint                `json:"patient_id"`
	Patient        User                `gorm:"foreignKey:PatientID"`
	ProfessionalID uint                `json:"professional_id"`
	Professional   ProfessionalProfile `gorm:"foreignKey:ProfessionalID;references:ID"`
	StartTime      time.Time           `json:"start_time"`
	EndTime        time.Time           `json:"end_time"`
	Status         string              `json:"status"`
	CreatedAt      time.Time           `json:"created_at"`
	UpdatedAt      time.Time           `json:"updated_at"`
}

type CreateAppointmentRequest struct {
	ProfessionalID uint   `json:"professional_id"`
	StartTime      string `json:"start_time"`
	EndTime        string `json:"end_time"`
}

type UpdateAppointmentRequest struct {
	StartTime string `json:"start_time"`
	EndTime   string `json:"end_time"`
	Status    string `json:"status"`
}

type AppointmentResponse struct {
	ID               uint      `json:"id"`
	PatientID        uint      `json:"patient_id"`
	PatientName      string    `json:"patient_name,omitempty"`
	ProfessionalID   uint      `json:"professional_id"`
	ProfessionalName string    `json:"professional_name,omitempty"`
	StartTime        time.Time `json:"start_time"`
	EndTime          time.Time `json:"end_time"`
	Status           string    `json:"status"`
}

func ToAppointmentResponse(a *Appointment) AppointmentResponse {
	return AppointmentResponse{
		ID:               a.ID,
		PatientID:        a.PatientID,
		PatientName:      a.Patient.Name,
		ProfessionalID:   a.ProfessionalID,
		ProfessionalName: a.Professional.User.Name,
		StartTime:        a.StartTime,
		EndTime:          a.EndTime,
		Status:           a.Status,
	}
}
