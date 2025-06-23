package handlers_test

import (
	"bytes"
	"encoding/json"
	"net/http/httptest"
	"testing"
	"vittaAqui/internal/config"
	"vittaAqui/internal/controller"
	"vittaAqui/internal/models"
	"vittaAqui/internal/services"

	"github.com/gofiber/fiber/v2"
	"github.com/stretchr/testify/assert"
)

// ---------------- MOCK -------------------

type MockUserService2 struct {
	services.UserService
	GetByIDFunc     func(uint) (*models.User, error)
	UpdateProfileFn func(uint, *models.UserUpdateRequest) (*models.User, error)
	DeleteUserFn    func(uint) error
	GetAllFunc      func() ([]models.User, error)
}

func (m *MockUserService2) GetByID(id uint) (*models.User, error) {
	if m.GetByIDFunc != nil {
		return m.GetByIDFunc(id)
	}
	return nil, nil
}

func (m *MockUserService2) UpdateProfile(id uint, req *models.UserUpdateRequest) (*models.User, error) {
	if m.UpdateProfileFn != nil {
		return m.UpdateProfileFn(id, req)
	}
	return nil, nil
}

func (m *MockUserService2) DeleteUser(id uint) error {
	if m.DeleteUserFn != nil {
		return m.DeleteUserFn(id)
	}
	return nil
}

func (m *MockUserService2) GetAll() ([]models.User, error) {
	if m.GetAllFunc != nil {
		return m.GetAllFunc()
	}
	return []models.User{}, nil
}

// ---------------- GetMe -------------------

func TestGetMeHandler(t *testing.T) {
	app := fiber.New()
	mockService := &MockUserService2{
		GetByIDFunc: func(id uint) (*models.User, error) {
			return &models.User{ID: id, Name: "Levi", Email: "levi@email.com", Role: "patient"}, nil
		},
	}

	testCfg := config.Config{JWTSecret: "secret-for-tests"}
	handler := controller.NewUserHandler(mockService, testCfg)
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
	handler := controller.NewUserHandler(mockService, testCfg)
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
	mockService := &MockUserService2{}
	testCfg := config.Config{JWTSecret: "secret-for-tests"}
	handler := controller.NewUserHandler(mockService, testCfg)
	app.Get("/user/me", handler.GetMe)

	req := httptest.NewRequest("GET", "/user/me", nil) // Sem user_id
	resp, _ := app.Test(req)
	assert.Equal(t, 401, resp.StatusCode)
}

// ---------------- Update -------------------

func TestUpdateMe_Success(t *testing.T) {
	app := fiber.New()
	mockService := &MockUserService2{
		UpdateProfileFn: func(id uint, req *models.UserUpdateRequest) (*models.User, error) {
			return &models.User{
				ID:    id,
				Name:  req.Name,
				Email: req.Email,
				Role:  models.Role(req.Role),
			}, nil
		},
	}
	testCfg := config.Config{JWTSecret: "secret-for-tests"}
	handler := controller.NewUserHandler(mockService, testCfg)

	app.Put("/user/me", func(c *fiber.Ctx) error {
		c.Locals("user_id", uint(1))
		return handler.UpdateMe(c)
	})

	body, _ := json.Marshal(models.UserUpdateRequest{
		Name:    "Levi Update",
		Email:   "levi@update.com",
		Role:    "patient",
		Phone:   "11999999999",
		CPF:     "12345678900",
		CEP:     "12345678",
		UF:      "SP",
		City:    "São Paulo",
		Address: "Rua XPTO",
	})

	req := httptest.NewRequest("PUT", "/user/me", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	resp, _ := app.Test(req)
	assert.Equal(t, 200, resp.StatusCode)
}

func TestUpdateMe_NotFound(t *testing.T) {
	app := fiber.New()
	mockService := &MockUserService2{
		UpdateProfileFn: func(id uint, req *models.UserUpdateRequest) (*models.User, error) {
			return nil, assert.AnError
		},
	}
	testCfg := config.Config{JWTSecret: "secret-for-tests"}
	handler := controller.NewUserHandler(mockService, testCfg)

	app.Put("/user/me", func(c *fiber.Ctx) error {
		c.Locals("user_id", uint(1))
		return handler.UpdateMe(c)
	})

	body := `{"name":"fail","email":"fail@email.com","role":"patient"}`
	req := httptest.NewRequest("PUT", "/user/me", bytes.NewBufferString(body))
	req.Header.Set("Content-Type", "application/json")
	resp, _ := app.Test(req)
	assert.Equal(t, 500, resp.StatusCode)
}

func TestUpdateMe_Unauthorized(t *testing.T) {
	app := fiber.New()
	mockService := &MockUserService2{}
	testCfg := config.Config{JWTSecret: "secret-for-tests"}
	handler := controller.NewUserHandler(mockService, testCfg)

	app.Put("/user/me", handler.UpdateMe)

	body := `{"name":"unauth","email":"unauth@email.com","role":"patient"}`
	req := httptest.NewRequest("PUT", "/user/me", bytes.NewBufferString(body))
	req.Header.Set("Content-Type", "application/json")
	resp, _ := app.Test(req)
	assert.Equal(t, 401, resp.StatusCode)
}

// ---------------- Delete -------------------

func TestDeleteMe_Success(t *testing.T) {
	app := fiber.New()
	mockService := &MockUserService2{
		DeleteUserFn: func(id uint) error {
			return nil
		},
	}
	testCfg := config.Config{JWTSecret: "secret-for-tests"}
	handler := controller.NewUserHandler(mockService, testCfg)

	app.Delete("/user/me", func(c *fiber.Ctx) error {
		c.Locals("user_id", uint(1))
		return handler.DeleteMe(c)
	})

	req := httptest.NewRequest("DELETE", "/user/me", nil)
	resp, _ := app.Test(req)
	assert.Equal(t, 200, resp.StatusCode)
}

func TestDeleteMe_NotFound(t *testing.T) {
	app := fiber.New()
	mockService := &MockUserService2{
		DeleteUserFn: func(id uint) error {
			return assert.AnError
		},
	}
	testCfg := config.Config{JWTSecret: "secret-for-tests"}
	handler := controller.NewUserHandler(mockService, testCfg)

	app.Delete("/user/me", func(c *fiber.Ctx) error {
		c.Locals("user_id", uint(1))
		return handler.DeleteMe(c)
	})

	req := httptest.NewRequest("DELETE", "/user/me", nil)
	resp, _ := app.Test(req)
	assert.Equal(t, 404, resp.StatusCode)
}

func TestDeleteMe_Unauthorized(t *testing.T) {
	app := fiber.New()
	mockService := &MockUserService2{}
	testCfg := config.Config{JWTSecret: "secret-for-tests"}
	handler := controller.NewUserHandler(mockService, testCfg)

	app.Delete("/user/me", handler.DeleteMe)

	req := httptest.NewRequest("DELETE", "/user/me", nil)
	resp, _ := app.Test(req)
	assert.Equal(t, 401, resp.StatusCode)
}
