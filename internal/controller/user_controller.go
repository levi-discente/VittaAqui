package controller

import (
	"strconv"

	"github.com/levirenato/VittaAqui/internal/config"
	"github.com/levirenato/VittaAqui/internal/models"
	"github.com/levirenato/VittaAqui/internal/services"

	"github.com/gofiber/fiber/v2"
)

type UserHandler struct {
	service services.UserServiceInterface
	cfg     config.Config
}

func NewUserHandler(service services.UserServiceInterface, cfg config.Config) *UserHandler {
	return &UserHandler{service, cfg}
}

// GetMe godoc
// @Summary      Pegar informações do usuário autenticado
// @Description  Retorna dados do próprio usuário (me)
// @Tags         user
// @Security     BearerAuth
// @Produce      json
// @Success      200  {object}  models.UserResponse
// @Failure      401  {object}  map[string]interface{}
// @Failure      404  {object}  map[string]interface{}
// @Router       /user/me [get]
func (h *UserHandler) GetMe(c *fiber.Ctx) error {
	uid, ok := c.Locals("user_id").(uint)
	if !ok {
		return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": "unauthorized"})
	}

	user, err := h.service.GetByID(uid)
	if err != nil || user == nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{"error": "user not found"})
	}

	return c.JSON(user.ToUserResponse())
}

// UpdateMe godoc
// @Summary      Atualizar dados do próprio usuário
// @Description  Permite atualizar informações pessoais do próprio usuário
// @Tags         user
// @Security     BearerAuth
// @Accept       json
// @Produce      json
// @Param        user  body      models.UserUpdateRequest  true  "Novos dados do usuário"
// @Success      200   {object}  models.UserResponse
// @Failure      400   {object}  map[string]interface{}
// @Failure      401   {object}  map[string]interface{}
// @Failure      500   {object}  map[string]interface{}
// @Router       /user/me [put]
func (h *UserHandler) UpdateMe(c *fiber.Ctx) error {
	uid, err := parseUserID(c)
	if err != nil {
		return err
	}

	var req models.UserUpdateRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "cannot parse JSON"})
	}

	user, err := h.service.UpdateProfile(uid, &req)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}
	return c.JSON(user.ToUserResponse())
}

// DeleteMe godoc
// @Summary      Deletar o próprio usuário
// @Description  Remove o próprio usuário autenticado do sistema
// @Tags         user
// @Security     BearerAuth
// @Produce      json
// @Success      200  {object}  map[string]interface{}
// @Failure      401  {object}  map[string]interface{}
// @Failure      404  {object}  map[string]interface{}
// @Router       /user/me [delete]
func (h *UserHandler) DeleteMe(c *fiber.Ctx) error {
	uid, err := parseUserID(c)
	if err != nil {
		return err
	}
	if err := h.service.DeleteUser(uid); err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{"error": "user not found"})
	}
	return c.JSON(fiber.Map{"message": "user deleted"})
}

// GetUserByID godoc
// @Summary      Buscar usuário por ID
// @Description  Retorna dados de um usuário específico (próprio usuário ou admin futuramente)
// @Tags         user
// @Security     BearerAuth
// @Produce      json
// @Param        id   path      int  true  "ID do usuário"
// @Success      200  {object}  models.UserResponse
// @Failure      400  {object}  map[string]interface{}
// @Failure      401  {object}  map[string]interface{}
// @Failure      403  {object}  map[string]interface{}
// @Failure      404  {object}  map[string]interface{}
// @Router       /user/{id} [get]
func (h *UserHandler) GetUserByID(c *fiber.Ctx) error {
	idParam := c.Params("id")
	id, err := strconv.ParseUint(idParam, 10, 32)
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "invalid id"})
	}

	uid, err := parseUserID(c)
	if err != nil {
		return err
	}

	// Permite acesso ao próprio usuário ou admin futuramente
	if uid != uint(id) {
		return c.Status(fiber.StatusForbidden).JSON(fiber.Map{"error": "forbidden"})
	}

	user, err := h.service.GetByID(uint(id))
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{"error": "user not found"})
	}
	return c.JSON(user.ToUserResponse())
}

// GetAllUsers godoc
// @Summary      Listar todos os usuários
// @Description  Retorna a lista de todos os usuários cadastrados (admin futuramente)
// @Tags         user
// @Security     BearerAuth
// @Produce      json
// @Success      200  {array}   models.UserResponse
// @Failure      401  {object}  map[string]interface{}
// @Failure      500  {object}  map[string]interface{}
// @Router       /user [get]
func (h *UserHandler) GetAllUsers(c *fiber.Ctx) error {
	users, err := h.service.GetAll()
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}
	var resp []models.UserResponse
	for _, user := range users {
		resp = append(resp, *user.ToUserResponse())
	}
	return c.JSON(resp)
}

func parseUserID(c *fiber.Ctx) (uint, error) {
	uid, ok := c.Locals("user_id").(uint)
	if ok {
		return uid, nil
	}
	idStr, ok := c.Locals("user_id").(string)
	if !ok {
		return 0, c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": "unauthorized"})
	}
	parsed, err := strconv.ParseUint(idStr, 10, 32)
	if err != nil {
		return 0, c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": "unauthorized"})
	}
	return uint(parsed), nil
}
