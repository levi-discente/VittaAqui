package handlers_test

import (
	"net/http/httptest"
	"net/url"
	"strings"
	"testing"
	"vittaAqui/internal/config"
	"vittaAqui/internal/handlers"
	"vittaAqui/internal/models"
	"vittaAqui/internal/services"

	"github.com/gofiber/fiber/v2"
	"github.com/stretchr/testify/assert"
)

// Mocks
type MockUserService struct {
	services.UserService
	RegisterFunc func(*models.UserRegisterRequest, string, string) error
	LoginFunc    func(string, string) (*models.User, error)
}

func (m *MockUserService) Register(req *models.UserRegisterRequest, bio, category string) error {
	return m.RegisterFunc(req, bio, category)
}

func (m *MockUserService) Login(email, password string) (*models.User, error) {
	return m.LoginFunc(email, password)
}

func TestRegisterHandler(t *testing.T) {
	app := fiber.New()
	mockService := &MockUserService{
		RegisterFunc: func(req *models.UserRegisterRequest, bio, category string) error {
			if req.Email == "error@email.com" {
				return assert.AnError
			}
			return nil
		},
	}
	testCfg := config.Config{JWTSecret: "secret-for-tests"}
	handler := handlers.NewUserHandler(mockService, testCfg)

	app.Post("/auth/register", handler.Register)

	form := url.Values{}
	form.Add("name", "Levi Teste")
	form.Add("email", "levi@email.com")
	form.Add("password", "123456")
	form.Add("role", "professional")
	form.Add("bio", "Sou fera")
	form.Add("category", "nutritionist")

	req := httptest.NewRequest("POST", "/auth/register", strings.NewReader(form.Encode()))
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")

	resp, _ := app.Test(req)
	assert.Equal(t, 200, resp.StatusCode)
}

func TestLoginHandler(t *testing.T) {
	app := fiber.New()
	mockService := &MockUserService{
		LoginFunc: func(email, password string) (*models.User, error) {
			if email == "fail@email.com" {
				return nil, assert.AnError
			}
			return &models.User{ID: 1, Email: email, Role: "patient"}, nil
		},
	}
	testCfg := config.Config{JWTSecret: "secret-for-tests"}
	handler := handlers.NewUserHandler(mockService, testCfg)

	app.Post("/auth/login", handler.Login)

	form := url.Values{}
	form.Add("email", "success@email.com")
	form.Add("password", "123456")

	req := httptest.NewRequest("POST", "/auth/login", strings.NewReader(form.Encode()))
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")

	resp, _ := app.Test(req)
	assert.Equal(t, 200, resp.StatusCode)
}

func TestRegisterHandler_Error(t *testing.T) {
	app := fiber.New()
	mockService := &MockUserService{
		RegisterFunc: func(req *models.UserRegisterRequest, bio, category string) error {
			return assert.AnError
		},
	}
	testCfg := config.Config{JWTSecret: "secret-for-tests"}
	handler := handlers.NewUserHandler(mockService, testCfg)

	app.Post("/auth/register", handler.Register)

	form := url.Values{}
	form.Add("name", "Error User")
	form.Add("email", "error@email.com")
	form.Add("password", "123456")
	form.Add("role", "professional")
	form.Add("bio", "Erro")
	form.Add("category", "nutritionist")

	req := httptest.NewRequest("POST", "/auth/register", strings.NewReader(form.Encode()))
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")

	resp, _ := app.Test(req)
	assert.Equal(t, 500, resp.StatusCode)
}

func TestRegisterHandler_MissingFields(t *testing.T) {
	app := fiber.New()
	mockService := &MockUserService{
		RegisterFunc: func(req *models.UserRegisterRequest, bio, category string) error {
			return nil
		},
	}
	testCfg := config.Config{JWTSecret: "secret-for-tests"}
	handler := handlers.NewUserHandler(mockService, testCfg)
	app.Post("/auth/register", handler.Register)

	form := url.Values{}
	form.Add("email", "fail@email.com")

	req := httptest.NewRequest("POST", "/auth/register", strings.NewReader(form.Encode()))
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	resp, _ := app.Test(req)
	assert.Equal(t, 400, resp.StatusCode)
}

func TestLoginHandler_Error(t *testing.T) {
	app := fiber.New()
	mockService := &MockUserService{
		LoginFunc: func(email, password string) (*models.User, error) {
			return nil, assert.AnError
		},
	}
	testCfg := config.Config{JWTSecret: "secret-for-tests"}
	handler := handlers.NewUserHandler(mockService, testCfg)
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
	mockService := &MockUserService{
		LoginFunc: func(email, password string) (*models.User, error) {
			return nil, nil
		},
	}
	testCfg := config.Config{JWTSecret: "secret-for-tests"}
	handler := handlers.NewUserHandler(mockService, testCfg)
	app.Post("/auth/login", handler.Login)

	form := url.Values{}
	req := httptest.NewRequest("POST", "/auth/login", strings.NewReader(form.Encode()))
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	resp, _ := app.Test(req)
	assert.Equal(t, 400, resp.StatusCode)
}
