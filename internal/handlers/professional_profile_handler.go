package handlers

import (
	"errors"
	"strconv"
	"strings"
	"vittaAqui/internal/models"
	"vittaAqui/internal/services"

	"github.com/gofiber/fiber/v2"
)

type ProfessionalProfileHandler struct {
	service services.ProfessionalProfileServiceInterface
}

func NewProfessionalProfileHandler(service services.ProfessionalProfileServiceInterface) *ProfessionalProfileHandler {
	return &ProfessionalProfileHandler{service}
}

// CreateProfile godoc
// @Summary      Cria perfil profissional
// @Tags         professional
// @Security     BearerAuth
// @Accept       json
// @Produce      json
// @Param        data body models.ProfessionalProfile true "Dados do perfil profissional"
// @Success      200 {object} models.ProfessionalProfileResponse
// @Failure      400 {object} map[string]interface{}
// @Failure      401 {object} map[string]interface{}
// @Router       /professional/profile [post]
func (h *ProfessionalProfileHandler) CreateProfile(c *fiber.Ctx) error {
	userID, ok := c.Locals("user_id").(uint)
	if !ok {
		return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": "unauthorized"})
	}
	var data models.ProfessionalProfile
	if err := c.BodyParser(&data); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "cannot parse JSON"})
	}
	if err := h.service.CreateProfile(userID, &data); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	resp := models.ToProfessionalProfileResponse(&data)
	return c.JSON(resp)
}

// GetByUserID godoc
// @Summary      Busca perfil profissional pelo userID
// @Tags         professional
// @Produce      json
// @Param        user_id path int true "ID do usuário"
// @Success      200 {object} models.ProfessionalProfileResponse
// @Failure      404 {object} map[string]interface{}
// @Router       /professional/profile/user/{user_id} [get]
func (h *ProfessionalProfileHandler) GetByUserID(c *fiber.Ctx) error {
	userID, err := strconv.Atoi(c.Params("user_id"))
	if err != nil {
		return c.Status(400).JSON(fiber.Map{"error": "invalid user_id"})
	}
	profile, err := h.service.GetByUserID(uint(userID))
	if err != nil {
		return c.Status(404).JSON(fiber.Map{"error": "profile not found"})
	}
	resp := models.ToProfessionalProfileResponse(profile)
	return c.JSON(resp)
}

// GetByProfessionalID godoc
// @Summary      Busca perfil profissional pelo profileID
// @Tags         professional
// @Produce      json
// @Param        id path int true "ID do perfil profissional"
// @Success      200 {object} models.ProfessionalProfileResponse
// @Failure      404 {object} map[string]interface{}
// @Router       /professional/profile/{id} [get]
func (h *ProfessionalProfileHandler) GetByProfessionalID(c *fiber.Ctx) error {
	profileID, err := strconv.Atoi(c.Params("id"))
	if err != nil {
		return c.Status(400).JSON(fiber.Map{"error": "invalid profile_id"})
	}
	profile, err := h.service.GetByProfessionalID(uint(profileID))
	if err != nil {
		return c.Status(404).JSON(fiber.Map{"error": "profile not found"})
	}
	resp := models.ToProfessionalProfileResponse(profile)
	return c.JSON(resp)
}

// ListProfessionals godoc
// @Summary      Lista perfis profissionais com filtros
// @Tags         professional
// @Produce      json
// @Param        category query string false "Categoria do profissional"
// @Param        name query string false "Nome do profissional"
// @Param        tags query string false "Tags separadas por vírgula"
// @Param        only_online query bool false "Apenas online"
// @Param        only_presential query bool false "Apenas presencial"
// @Success      200 {array} models.ProfessionalProfileResponse
// @Router       /professional/list [get]
func (h *ProfessionalProfileHandler) ListProfessionals(c *fiber.Ctx) error {
	category := c.Query("category", "")
	name := c.Query("name", "")
	tagsStr := c.Query("tags", "")
	var tags []string
	if tagsStr != "" {
		for _, tag := range strings.Split(tagsStr, ",") {
			tag = strings.TrimSpace(tag)
			if tag != "" {
				tags = append(tags, tag)
			}
		}
	}
	var onlyOnlinePtr, onlyPresentialPtr *bool
	if o := c.Query("only_online"); o != "" {
		val := o == "true" || o == "1"
		onlyOnlinePtr = &val
	}
	if o := c.Query("only_presential"); o != "" {
		val := o == "true" || o == "1"
		onlyPresentialPtr = &val
	}
	profiles, err := h.service.ListProfessionals(category, name, tags, onlyOnlinePtr, onlyPresentialPtr)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{"error": err.Error()})
	}
	var resp []models.ProfessionalProfileResponse
	for _, p := range profiles {
		resp = append(resp, models.ToProfessionalProfileResponse(&p))
	}
	return c.JSON(resp)
}

// EditProfile godoc
// @Summary      Edita perfil profissional (owner only)
// @Tags         professional
// @Security     BearerAuth
// @Accept       json
// @Produce      json
// @Param        id path int true "ID do perfil profissional"
// @Param        data body models.ProfessionalProfile true "Novos dados do perfil"
// @Success      200 {object} models.ProfessionalProfileResponse
// @Failure      400 {object} map[string]interface{}
// @Failure      401 {object} map[string]interface{}
// @Router       /professional/profile/{id} [put]
func (h *ProfessionalProfileHandler) EditProfile(c *fiber.Ctx) error {
	userID, ok := c.Locals("user_id").(uint)
	if !ok {
		return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": "unauthorized"})
	}
	profileID, err := strconv.Atoi(c.Params("id"))
	if err != nil {
		return c.Status(400).JSON(fiber.Map{"error": "invalid profile_id"})
	}
	var data models.ProfessionalProfile
	if err := c.BodyParser(&data); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "cannot parse JSON"})
	}
	err = h.service.EditProfile(userID, uint(profileID), &data)
	if err != nil {
		if errors.Is(err, services.ErrNotProfileOwner) {
			return c.Status(fiber.StatusForbidden).JSON(fiber.Map{"error": err.Error()})
		}
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}
	updated, _ := h.service.GetByProfessionalID(uint(profileID))
	resp := models.ToProfessionalProfileResponse(updated)
	return c.JSON(resp)
}

// DeleteProfile godoc
// @Summary      Remove perfil profissional (owner only)
// @Tags         professional
// @Security     BearerAuth
// @Produce      json
// @Param        id path int true "ID do perfil profissional"
// @Success      200 {object} map[string]interface{}
// @Failure      401 {object} map[string]interface{}
// @Failure      403 {object} map[string]interface{}
// @Router       /professional/profile/{id} [delete]
func (h *ProfessionalProfileHandler) DeleteProfile(c *fiber.Ctx) error {
	userID, ok := c.Locals("user_id").(uint)
	if !ok {
		return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": "unauthorized"})
	}
	profileID, err := strconv.Atoi(c.Params("id"))
	if err != nil {
		return c.Status(400).JSON(fiber.Map{"error": "invalid profile_id"})
	}
	err = h.service.DeleteProfile(userID, uint(profileID))
	if err != nil {
		if errors.Is(err, services.ErrNotProfileOwner) {
			return c.Status(fiber.StatusForbidden).JSON(fiber.Map{"error": err.Error()})
		}
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}
	return c.JSON(fiber.Map{"message": "profile deleted"})
}
