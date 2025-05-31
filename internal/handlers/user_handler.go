package handlers

import (
	"strconv"
	"vittaAqui/internal/config"
	"vittaAqui/internal/models"
	"vittaAqui/internal/services"

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
// @Accept       json
// @Produce      json
// @Success      200  {object}  models.UserResponse
// @Failure      401  {object}  map[string]interface{}
// @Router       /user/me [get]
func (h *UserHandler) GetMe(c *fiber.Ctx) error {
	uid, ok := c.Locals("user_id").(uint)
	if !ok {
		// Suporte para conversão de string, dependendo do middleware
		idStr, ok := c.Locals("user_id").(string)
		if !ok {
			return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": "unauthorized"})
		}
		parsed, err := strconv.ParseUint(idStr, 10, 32)
		if err != nil {
			return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": "unauthorized"})
		}
		uid = uint(parsed)
	}
	user, err := h.service.GetByID(uid)
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{"error": "user not found"})
	}
	return c.JSON(models.UserResponse{
		ID:    user.ID,
		Name:  user.Name,
		Email: user.Email,
		Role:  string(user.Role),
	})
}

// UpdateMe godoc
// @Summary      Atualizar usuário autenticado
// @Description  Atualiza dados do próprio usuário
// @Tags         user
// @Security     BearerAuth
// @Accept       json
// @Produce      json
// @Param        user  body      models.UserUpdateRequest  true  "Novos dados"
// @Success      200   {object}  models.UserResponse
// @Failure      400   {object}  map[string]interface{}
// @Failure      401   {object}  map[string]interface{}
// @Router       /user/me [put]
func (h *UserHandler) UpdateMe(c *fiber.Ctx) error {
	uid, ok := c.Locals("user_id").(uint)
	if !ok {
		idStr, ok := c.Locals("user_id").(string)
		if !ok {
			return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": "unauthorized"})
		}
		parsed, err := strconv.ParseUint(idStr, 10, 32)
		if err != nil {
			return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": "unauthorized"})
		}
		uid = uint(parsed)
	}
	var req models.UserUpdateRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "cannot parse JSON"})
	}
	user, err := h.service.UpdateProfile(uid, &req)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}
	return c.JSON(models.UserResponse{
		ID:    user.ID,
		Name:  user.Name,
		Email: user.Email,
		Role:  string(user.Role),
	})
}

// DeleteMe godoc
// @Summary      Deletar o próprio usuário
// @Description  Remove o próprio usuário autenticado
// @Tags         user
// @Security     BearerAuth
// @Accept       json
// @Produce      json
// @Success      200  {object}  map[string]interface{}
// @Failure      401  {object}  map[string]interface{}
// @Failure      404  {object}  map[string]interface{}
// @Router       /user/me [delete]
func (h *UserHandler) DeleteMe(c *fiber.Ctx) error {
	uid, ok := c.Locals("user_id").(uint)
	if !ok {
		idStr, ok := c.Locals("user_id").(string)
		if !ok {
			return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": "unauthorized"})
		}
		parsed, err := strconv.ParseUint(idStr, 10, 32)
		if err != nil {
			return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": "unauthorized"})
		}
		uid = uint(parsed)
	}
	if err := h.service.DeleteUser(uid); err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{"error": "user not found"})
	}
	return c.JSON(fiber.Map{"message": "user deleted"})
}

// GetUserByID godoc
// @Summary      Buscar usuário por ID (admin)
// @Description  Retorna dados de um usuário específico (acesso restrito)
// @Tags         user
// @Security     BearerAuth
// @Accept       json
// @Produce      json
// @Param        id   path      int  true  "ID do usuário"
// @Success      200  {object}  models.UserResponse
// @Failure      401  {object}  map[string]interface{}
// @Failure      404  {object}  map[string]interface{}
// @Router       /user/{id} [get]
func (h *UserHandler) GetUserByID(c *fiber.Ctx) error {
	// Exemplo: restrinja a admin ou ao próprio user
	idParam := c.Params("id")
	id, err := strconv.ParseUint(idParam, 10, 32)
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "invalid id"})
	}
	uid, ok := c.Locals("user_id").(uint)
	if !ok {
		idStr, ok := c.Locals("user_id").(string)
		if !ok {
			return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": "unauthorized"})
		}
		parsed, err := strconv.ParseUint(idStr, 10, 32)
		if err != nil {
			return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": "unauthorized"})
		}
		uid = uint(parsed)
	}
	// Só permite acesso ao próprio usuário ou admin
	if uid != uint(id) /* && !isAdmin(c) */ {
		return c.Status(fiber.StatusForbidden).JSON(fiber.Map{"error": "forbidden"})
	}
	user, err := h.service.GetByID(uint(id))
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{"error": "user not found"})
	}
	return c.JSON(models.UserResponse{
		ID:    user.ID,
		Name:  user.Name,
		Email: user.Email,
		Role:  string(user.Role),
	})
}

// GetAllUsers godoc
// @Summary      Listar todos os usuários (admin)
// @Description  Retorna todos os usuários cadastrados (acesso restrito)
// @Tags         user
// @Security     BearerAuth
// @Accept       json
// @Produce      json
// @Success      200  {array}   models.UserResponse
// @Failure      401  {object}  map[string]interface{}
// @Router       /user [get]
func (h *UserHandler) GetAllUsers(c *fiber.Ctx) error {
	// Exemplo: restrinja a admin
	// if !isAdmin(c) { return c.Status(fiber.StatusForbidden).JSON(fiber.Map{"error": "forbidden"}) }
	users, err := h.service.GetAll()
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}
	var resp []models.UserResponse
	for _, user := range users {
		resp = append(resp, models.UserResponse{
			ID:    user.ID,
			Name:  user.Name,
			Email: user.Email,
			Role:  string(user.Role),
		})
	}
	return c.JSON(resp)
}
