package controller

import (
	"errors"
	"time"

	"github.com/levirenato/VittaAqui/internal/models"
	"github.com/levirenato/VittaAqui/internal/services"

	"github.com/gofiber/fiber/v2"
	"github.com/golang-jwt/jwt/v5"
)

// Register godoc
// @Summary      Cadastro de usuário
// @Description  Cria um novo usuário no sistema (profissional já cria perfil)
// @Tags         auth
// @Accept       x-www-form-urlencoded
// @Produce      json
// @Param        name     formData string true "Nome"
// @Param        email    formData string true "Email"
// @Param        password formData string true "Senha"
// @Param        role     formData string true "Role (patient/professional)"
// @Param        bio      formData string false "Bio do profissional (se profissional)"
// @Param        category formData string false "Categoria profissional (se profissional)"
// @Success      200   {object}  map[string]interface{}
// @Failure      400   {object}  map[string]interface{}
// @Failure      500   {object}  map[string]interface{}
// @Router       /auth/register [post]
func (h *UserHandler) Register(c *fiber.Ctx) error {
	name := c.FormValue("name")
	email := c.FormValue("email")
	password := c.FormValue("password")
	role := c.FormValue("role")
	cpf := c.FormValue("cpf")
	phone := c.FormValue("phone")
	cep := c.FormValue("cep")
	uf := c.FormValue("uf")
	city := c.FormValue("city")
	address := c.FormValue("address")

	if name == "" || email == "" || password == "" || role == "" || cpf == "" {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "missing required fields"})
	}

	req := models.UserRegisterRequest{
		Name:     name,
		Email:    email,
		Password: password,
		Role:     role,
		CPF:      cpf,
		Phone:    phone,
		CEP:      cep,
		UF:       uf,
		City:     city,
		Address:  address,
	}

	bio := c.FormValue("bio")
	category := c.FormValue("category")

	if err := h.service.Register(&req, bio, category); err != nil {

		if errors.Is(err, services.ErrCPFAlreadyExists) ||
			errors.Is(err, services.ErrEmailAlreadyExists) ||
			errors.Is(err, services.ErrInvalidCPF) {
			return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
		}

		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(fiber.Map{"message": "registered"})
}

// Login godoc
// @Summary      Login de usuário
// @Description  Autentica o usuário e retorna o token JWT
// @Tags         auth
// @Accept       x-www-form-urlencoded
// @Produce      json
// @Param        email    formData string true "Email"
// @Param        password formData string true "Senha"
// @Success      200    {object}  models.LoginResponse
// @Failure      400    {object}  map[string]interface{}
// @Failure      401    {object}  map[string]interface{}
// @Router       /auth/login [post]
func (h *UserHandler) Login(c *fiber.Ctx) error {
	email := c.FormValue("email")
	password := c.FormValue("password")

	if email == "" || password == "" {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "missing email or password"})
	}

	user, err := h.service.Login(email, password)
	if err != nil {
		return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": "invalid credentials"})
	}
	claims := jwt.MapClaims{
		"user": user.ToUserResponse(),
		"exp":  time.Now().Add(time.Hour * 24).Unix(),
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	t, err := token.SignedString([]byte(h.cfg.JWTSecret))
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "could not login"})
	}
	return c.JSON(models.LoginResponse{Token: t, User: models.UserResponse{ID: user.ID, Name: user.Name, Email: user.Email, Role: string(user.Role)}})
}
