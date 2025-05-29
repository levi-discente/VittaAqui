package handlers

import (
	"time"
	"vittaAqui/internal/models"

	"github.com/gofiber/fiber/v2"
	"github.com/golang-jwt/jwt/v5"
)

// Register godoc
// @Summary      Cadastro de usuário
// @Description  Cria um novo usuário no sistema
// @Tags         auth
// @Accept       json
// @Produce      json
// @Param        user  body      models.UserRegisterRequest  true  "Dados do usuário"
// @Success      200   {object}  map[string]interface{}
// @Failure      400   {object}  map[string]interface{}
// @Failure      500   {object}  map[string]interface{}
// @Router       /auth/register [post]
func (h *UserHandler) Register(c *fiber.Ctx) error {
	user := new(models.UserRegisterRequest)
	if err := c.BodyParser(user); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "cannot parse JSON"})
	}
	if err := h.service.Register(&models.User{
		Name:     user.Name,
		Email:    user.Email,
		Password: user.Password,
		Role:     user.Role,
	}); err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}
	return c.JSON(fiber.Map{"message": "registered"})
}

// Login godoc
// @Summary      Login de usuário
// @Description  Autentica o usuário e retorna o token JWT
// @Tags         auth
// @Accept       json
// @Produce      json
// @Param        login  body      models.UserLoginRequest  true  "Credenciais do usuário"
// @Success      200    {object}  models.LoginResponse
// @Failure      400    {object}  map[string]interface{}
// @Failure      401    {object}  map[string]interface{}
// @Router       /auth/login [post]
func (h *UserHandler) Login(c *fiber.Ctx) error {
	req := new(models.UserLoginRequest)
	if err := c.BodyParser(req); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "cannot parse JSON"})
	}
	user, err := h.service.Login(req.Email, req.Password)
	if err != nil {
		return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": "invalid credentials"})
	}
	claims := jwt.MapClaims{
		"id":    user.ID,
		"email": user.Email,
		"role":  user.Role,
		"exp":   time.Now().Add(time.Hour * 24).Unix(),
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	t, err := token.SignedString([]byte(h.cfg.JWTSecret))
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "could not login"})
	}
	return c.JSON(models.LoginResponse{Token: t})
}
