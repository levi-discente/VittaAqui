package handlers_test

import (
	"net/http/httptest"
	"testing"
	"vittaAqui/internal/config"
	"vittaAqui/internal/handlers"
	"vittaAqui/internal/models"
	"vittaAqui/internal/services"

	"github.com/gofiber/fiber/v2"
	"github.com/stretchr/testify/assert"
)

type MockUserService2 struct {
	services.UserService
	GetByIDFunc     func(uint) (*models.User, error)
	UpdateProfileFn func(uint, *models.UserUpdateRequest) (*models.User, error)
	DeleteUserFn    func(uint) error
	GetAllFunc      func() ([]models.User, error)
}

func (m *MockUserService2) GetByID(id uint) (*models.User, error) { return m.GetByIDFunc(id) }
func (m *MockUserService2) UpdateProfile(id uint, req *models.UserUpdateRequest) (*models.User, error) {
	return m.UpdateProfileFn(id, req)
}
func (m *MockUserService2) DeleteUser(id uint) error       { return m.DeleteUserFn(id) }
func (m *MockUserService2) GetAll() ([]models.User, error) { return m.GetAllFunc() }

func TestGetMeHandler(t *testing.T) {
	app := fiber.New()
	mockService := &MockUserService2{
		GetByIDFunc: func(id uint) (*models.User, error) {
			return &models.User{ID: id, Name: "Levi", Email: "levi@email.com", Role: "patient"}, nil
		},
	}

	testCfg := config.Config{JWTSecret: "secret-for-tests"}
	handler := handlers.NewUserHandler(mockService, testCfg)
	app.Get("/user/me", func(c *fiber.Ctx) error {
		c.Locals("user_id", uint(123))
		return handler.GetMe(c)
	})

	req := httptest.NewRequest("GET", "/user/me", nil)
	resp, _ := app.Test(req)
	assert.Equal(t, 200, resp.StatusCode)
}

func TestGetMeHandler_NotFound(t *testing.T) {
	app := fiber.New()
	mockService := &MockUserService2{
		GetByIDFunc: func(id uint) (*models.User, error) {
			return nil, assert.AnError
		},
	}
	testCfg := config.Config{JWTSecret: "secret-for-tests"}
	handler := handlers.NewUserHandler(mockService, testCfg)
	app.Get("/user/me", func(c *fiber.Ctx) error {
		c.Locals("user_id", uint(123))
		return handler.GetMe(c)
	})

	req := httptest.NewRequest("GET", "/user/me", nil)
	resp, _ := app.Test(req)
	assert.Equal(t, 404, resp.StatusCode)
}

func TestGetMeHandler_Unauthorized(t *testing.T) {
	app := fiber.New()
	mockService := &MockUserService2{
		GetByIDFunc: func(id uint) (*models.User, error) {
			return &models.User{ID: id, Name: "Levi"}, nil
		},
	}
	testCfg := config.Config{JWTSecret: "secret-for-tests"}
	handler := handlers.NewUserHandler(mockService, testCfg)
	app.Get("/user/me", handler.GetMe)

	req := httptest.NewRequest("GET", "/user/me", nil) // no user_id set
	resp, _ := app.Test(req)
	assert.Equal(t, 401, resp.StatusCode)
}
