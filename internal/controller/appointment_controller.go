package controller

import (
	"strconv"
	"time"

	"github.com/gofiber/fiber/v2"
	"github.com/levirenato/VittaAqui/internal/models"
	"github.com/levirenato/VittaAqui/internal/services"
)

type AppointmentHandler struct {
	service *services.AppointmentService
}

func NewAppointmentHandler(service *services.AppointmentService) *AppointmentHandler {
	return &AppointmentHandler{service}
}

// CreateAppointment godoc
// @Summary Cria um novo agendamento
// @Tags appointment
// @Security BearerAuth
// @Accept json
// @Produce json
// @Param data body models.CreateAppointmentRequest true "Dados do agendamento"
// @Success 200 {object} models.AppointmentResponse
// @Failure 400 {object} map[string]interface{}
// @Failure 409 {object} map[string]interface{}
// @Router /appointments [post]
func (h *AppointmentHandler) CreateAppointment(c *fiber.Ctx) error {
	patientID := c.Locals("user_id").(uint)

	var req models.CreateAppointmentRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "invalid request"})
	}

	start, err1 := time.Parse(time.RFC3339Nano, req.StartTime)
	end, err2 := time.Parse(time.RFC3339Nano, req.EndTime)
	if err1 != nil || err2 != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error":       "invalid time format",
			"start_input": req.StartTime,
			"end_input":   req.EndTime,
			"req":         req,
		})
	}

	err := h.service.CreateAppointment(patientID, req.ProfessionalID, start, end)
	if err != nil {
		if err == services.ErrTimeConflict {
			return c.Status(fiber.StatusConflict).JSON(fiber.Map{"error": "time conflict"})
		}
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(fiber.StatusCreated).JSON(fiber.Map{
		"message": "appointment created successfully",
	})
}

// GetMyAppointments godoc
// @Summary Lista agendamentos do paciente logado
// @Tags appointment
// @Security BearerAuth
// @Produce json
// @Success 200 {array} models.AppointmentResponse
// @Router /appointments/my [get]
func (h *AppointmentHandler) GetMyAppointments(c *fiber.Ctx) error {
	userID := c.Locals("user_id").(uint)

	list, err := h.service.GetPatientAppointments(userID)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	var resp []models.AppointmentResponse
	for _, ap := range list {
		resp = append(resp, models.ToAppointmentResponse(&ap))
	}

	return c.JSON(resp)
}

// GetProfessionalSchedule godoc
// @Summary Lista agendamentos de um profissional
// @Tags appointment
// @Produce json
// @Param id path int true "ID do profissional"
// @Success 200 {array} models.AppointmentResponse
// @Failure 400 {object} map[string]interface{}
// @Router /appointments/professional/{id} [get]
func (h *AppointmentHandler) GetProfessionalSchedule(c *fiber.Ctx) error {
	professionalID, err := strconv.Atoi(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "invalid id"})
	}

	list, err := h.service.GetAppointmentsByProfessional(uint(professionalID))
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	var resp []models.AppointmentResponse
	for _, ap := range list {
		resp = append(resp, models.ToAppointmentResponse(&ap))
	}

	return c.JSON(resp)
}

// UpdateAppointment godoc
// @Summary Atualiza um agendamento
// @Tags appointment
// @Security BearerAuth
// @Accept json
// @Produce json
// @Param id path int true "ID do agendamento"
// @Param data body models.UpdateAppointmentRequest true "Novos dados do agendamento"
// @Success 200 {object} models.AppointmentResponse
// @Failure 400 {object} map[string]interface{}
// @Failure 409 {object} map[string]interface{}
// @Router /appointments/{id} [put]
func (h *AppointmentHandler) UpdateAppointment(c *fiber.Ctx) error {
	appointmentID, _ := strconv.Atoi(c.Params("id"))

	var req models.UpdateAppointmentRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "invalid body"})
	}

	start, err1 := time.Parse(time.RFC3339, req.StartTime)
	end, err2 := time.Parse(time.RFC3339, req.EndTime)
	if err1 != nil || err2 != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "invalid date format"})
	}

	err := h.service.UpdateAppointment(uint(appointmentID), start, end, req.Status)
	if err != nil {
		if err == services.ErrTimeConflict {
			return c.Status(fiber.StatusConflict).JSON(fiber.Map{"error": "time conflict"})
		}
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	updated, _ := h.service.GetAppointmentsByPatient(c.Locals("user_id").(uint))
	for _, ap := range updated {
		if ap.ID == uint(appointmentID) {
			return c.JSON(models.ToAppointmentResponse(&ap))
		}
	}

	return c.Status(fiber.StatusNotFound).JSON(fiber.Map{"error": "appointment not found"})
}

// DeleteAppointment godoc
// @Summary Remove um agendamento
// @Tags appointment
// @Security BearerAuth
// @Produce json
// @Param id path int true "ID do agendamento"
// @Success 200 {object} map[string]interface{}
// @Router /appointments/{id} [delete]
func (h *AppointmentHandler) DeleteAppointment(c *fiber.Ctx) error {
	appointmentID, _ := strconv.Atoi(c.Params("id"))

	err := h.service.DeleteAppointment(uint(appointmentID))
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(fiber.Map{"message": "appointment deleted"})
}
