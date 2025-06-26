package handlers_test

import (
	"net/http/httptest"
	"net/url"
	"strings"
	"testing"

	"github.com/levirenato/VittaAqui/internal/config"
	"github.com/levirenato/VittaAqui/internal/controller"
	"github.com/levirenato/VittaAqui/internal/models"
	"github.com/levirenato/VittaAqui/internal/services"

	"github.com/gofiber/fiber/v2"
	"github.com/stretchr/testify/assert"
)

// ----------------- MOCK -----------------

type MockUserService struct {
	services.UserService
	RegisterFunc func(*models.UserRegisterRequest, string, string) error
	LoginFunc    func(string, string) (*models.User, error)
}

func (m *MockUserService) Register(req *models.UserRegisterRequest, bio, category string) error {
	if m.RegisterFunc != nil {
		return m.RegisterFunc(req, bio, category)
	}

	if req.CPF == "11111111111" {
		return services.ErrInvalidCPF
	}
	if req.Email == "emailjaexiste@email.com" {
		return services.ErrEmailAlreadyExists
	}
	if req.CPF == "12345678909" && req.Email == "cpfjaexiste@email.com" {
		return services.ErrCPFAlreadyExists
	}

	return nil
}

func (m *MockUserService) Login(email, password string) (*models.User, error) {
	if m.LoginFunc != nil {
		return m.LoginFunc(email, password)
	}
	return &models.User{ID: 1, Email: email, Role: "patient"}, nil
}

// ----------------- REGISTER -----------------

func TestRegisterHandler_Success(t *testing.T) {
	app := fiber.New()
	mockService := &MockUserService{
		RegisterFunc: func(req *models.UserRegisterRequest, bio, category string) error {
			return nil
		},
	}
	testCfg := config.Config{JWTSecret: "secret-for-tests"}
	handler := controller.NewUserHandler(mockService, testCfg)

	app.Post("/auth/register", handler.Register)

	form := url.Values{}
	form.Add("name", "Levi Teste")
	form.Add("email", "levi@email.com")
	form.Add("cpf", "12345678909")
	form.Add("password", "123456")
	form.Add("role", "professional")
	form.Add("bio", "Sou fera")
	form.Add("category", "nutritionist")

	req := httptest.NewRequest("POST", "/auth/register", strings.NewReader(form.Encode()))
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")

	resp, _ := app.Test(req)
	assert.Equal(t, 200, resp.StatusCode)
}

func TestRegisterHandler_CPFInvalid(t *testing.T) {
	app := fiber.New()
	mockService := &MockUserService{}
	testCfg := config.Config{JWTSecret: "secret-for-tests"}
	handler := controller.NewUserHandler(mockService, testCfg)

	app.Post("/auth/register", handler.Register)

	form := url.Values{}
	form.Add("name", "Levi")
	form.Add("email", "levi@email.com")
	form.Add("cpf", "11111111111") // CPF inválido
	form.Add("password", "123456")
	form.Add("role", "professional")
	form.Add("bio", "Sou fera")
	form.Add("category", "nutritionist")

	req := httptest.NewRequest("POST", "/auth/register", strings.NewReader(form.Encode()))
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")

	resp, _ := app.Test(req)
	assert.Equal(t, 400, resp.StatusCode)
}

func TestRegisterHandler_EmailExists(t *testing.T) {
	app := fiber.New()
	mockService := &MockUserService{
		RegisterFunc: func(req *models.UserRegisterRequest, bio, category string) error {
			return services.ErrEmailAlreadyExists
		},
	}
	testCfg := config.Config{JWTSecret: "secret-for-tests"}
	handler := controller.NewUserHandler(mockService, testCfg)

	app.Post("/auth/register", handler.Register)

	form := url.Values{}
	form.Add("name", "Levi")
	form.Add("email", "emailjaexiste@email.com")
	form.Add("cpf", "12345678909")
	form.Add("password", "123456")
	form.Add("role", "professional")
	form.Add("bio", "Sou fera")
	form.Add("category", "nutritionist")

	req := httptest.NewRequest("POST", "/auth/register", strings.NewReader(form.Encode()))
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")

	resp, _ := app.Test(req)
	assert.Equal(t, 400, resp.StatusCode)
}

func TestRegisterHandler_CPFExists(t *testing.T) {
	app := fiber.New()
	mockService := &MockUserService{
		RegisterFunc: func(req *models.UserRegisterRequest, bio, category string) error {
			return services.ErrCPFAlreadyExists
		},
	}
	testCfg := config.Config{JWTSecret: "secret-for-tests"}
	handler := controller.NewUserHandler(mockService, testCfg)

	app.Post("/auth/register", handler.Register)

	form := url.Values{}
	form.Add("name", "Levi")
	form.Add("email", "levi@email.com")
	form.Add("cpf", "12345678909")
	form.Add("password", "123456")
	form.Add("role", "professional")
	form.Add("bio", "Sou fera")
	form.Add("category", "nutritionist")

	req := httptest.NewRequest("POST", "/auth/register", strings.NewReader(form.Encode()))
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")

	resp, _ := app.Test(req)
	assert.Equal(t, 400, resp.StatusCode)
}

func TestRegisterHandler_MissingFields(t *testing.T) {
	app := fiber.New()
	mockService := &MockUserService{}
	testCfg := config.Config{JWTSecret: "secret-for-tests"}
	handler := controller.NewUserHandler(mockService, testCfg)

	app.Post("/auth/register", handler.Register)

	form := url.Values{}
	form.Add("email", "fail@email.com") // Campos faltando

	req := httptest.NewRequest("POST", "/auth/register", strings.NewReader(form.Encode()))
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")

	resp, _ := app.Test(req)
	assert.Equal(t, 400, resp.StatusCode)
}

func TestRegisterHandler_ErrorGeneric(t *testing.T) {
	app := fiber.New()
	mockService := &MockUserService{
		RegisterFunc: func(req *models.UserRegisterRequest, bio, category string) error {
			return assert.AnError
		},
	}
	testCfg := config.Config{JWTSecret: "secret-for-tests"}
	handler := controller.NewUserHandler(mockService, testCfg)

	app.Post("/auth/register", handler.Register)

	form := url.Values{}
	form.Add("name", "Error User")
	form.Add("email", "error@email.com")
	form.Add("cpf", "12345678909")
	form.Add("password", "123456")
	form.Add("role", "professional")
	form.Add("bio", "Erro")
	form.Add("category", "nutritionist")

	req := httptest.NewRequest("POST", "/auth/register", strings.NewReader(form.Encode()))
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")

	resp, _ := app.Test(req)
	assert.Equal(t, 500, resp.StatusCode)
}

// ----------------- LOGIN -----------------

func TestLoginHandler_Success(t *testing.T) {
	app := fiber.New()
	mockService := &MockUserService{
		LoginFunc: func(email, password string) (*models.User, error) {
			return &models.User{ID: 1, Email: email, Role: "patient"}, nil
		},
	}
	testCfg := config.Config{JWTSecret: "secret-for-tests"}
	handler := controller.NewUserHandler(mockService, testCfg)

	app.Post("/auth/login", handler.Login)

	form := url.Values{}
	form.Add("email", "success@email.com")
	form.Add("password", "123456")

	req := httptest.NewRequest("POST", "/auth/login", strings.NewReader(form.Encode()))
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")

	resp, _ := app.Test(req)
	assert.Equal(t, 200, resp.StatusCode)
}

func TestLoginHandler_Error(t *testing.T) {
	app := fiber.New()
	mockService := &MockUserService{
		LoginFunc: func(email, password string) (*models.User, error) {
			return nil, assert.AnError
		},
	}
	testCfg := config.Config{JWTSecret: "secret-for-tests"}
	handler := controller.NewUserHandler(mockService, testCfg)

	app.Post("/auth/login", handler.Login)

	form := url.Values{}
	form.Add("email", "fail@email.com")
	form.Add("password", "wrong")

	req := httptest.NewRequest("POST", "/auth/login", strings.NewReader(form.Encode()))
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")

	resp, _ := app.Test(req)
	assert.Equal(t, 401, resp.StatusCode)
}

func TestLoginHandler_MissingFields(t *testing.T) {
	app := fiber.New()
	mockService := &MockUserService{}
	testCfg := config.Config{JWTSecret: "secret-for-tests"}
	handler := controller.NewUserHandler(mockService, testCfg)

	app.Post("/auth/login", handler.Login)

	form := url.Values{}

	req := httptest.NewRequest("POST", "/auth/login", strings.NewReader(form.Encode()))
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")

	resp, _ := app.Test(req)
	assert.Equal(t, 400, resp.StatusCode)
}
