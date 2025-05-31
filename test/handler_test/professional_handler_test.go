package handlers_test

import (
	"encoding/json"
	"errors"
	"net/http/httptest"
	"strings"
	"testing"
	"vittaAqui/internal/handlers"
	"vittaAqui/internal/models"
	"vittaAqui/internal/services"

	"github.com/gofiber/fiber/v2"
	"github.com/stretchr/testify/assert"
	"gorm.io/gorm"
)

// Mock do ProfessionalProfileService
type MockProfessionalProfileService struct {
	CreateProfileFunc       func(userID uint, profile *models.ProfessionalProfile) error
	GetByUserIDFunc         func(userID uint) (*models.ProfessionalProfile, error)
	GetByProfessionalIDFunc func(profileID uint) (*models.ProfessionalProfile, error)
	ListProfessionalsFunc   func(category, name string, tags []string, onlyOnline, onlyPresential *bool) ([]models.ProfessionalProfile, error)
	EditProfileFunc         func(userID, profileID uint, data *models.ProfessionalProfile) error
	DeleteProfileFunc       func(userID, profileID uint) error
}

func (m *MockProfessionalProfileService) CreateProfile(userID uint, profile *models.ProfessionalProfile) error {
	return m.CreateProfileFunc(userID, profile)
}

func (m *MockProfessionalProfileService) GetByUserID(userID uint) (*models.ProfessionalProfile, error) {
	return m.GetByUserIDFunc(userID)
}

func (m *MockProfessionalProfileService) GetByProfessionalID(profileID uint) (*models.ProfessionalProfile, error) {
	return m.GetByProfessionalIDFunc(profileID)
}

func (m *MockProfessionalProfileService) ListProfessionals(category, name string, tags []string, onlyOnline, onlyPresential *bool) ([]models.ProfessionalProfile, error) {
	return m.ListProfessionalsFunc(category, name, tags, onlyOnline, onlyPresential)
}

func (m *MockProfessionalProfileService) EditProfile(userID, profileID uint, data *models.ProfessionalProfile) error {
	return m.EditProfileFunc(userID, profileID, data)
}

func (m *MockProfessionalProfileService) DeleteProfile(userID, profileID uint) error {
	return m.DeleteProfileFunc(userID, profileID)
}

func TestCreateProfile(t *testing.T) {
	app := fiber.New()
	mockService := &MockProfessionalProfileService{
		CreateProfileFunc: func(userID uint, profile *models.ProfessionalProfile) error {
			return nil
		},
	}
	handler := handlers.NewProfessionalProfileHandler(mockService)
	app.Post("/professional/profile", func(c *fiber.Ctx) error {
		c.Locals("user_id", uint(1))
		return handler.CreateProfile(c)
	})

	body := `{"bio":"Test Bio","category":"nutritionist","services":"A,B,C","price":100.0,"only_online":true,"only_presential":false}`
	req := httptest.NewRequest("POST", "/professional/profile", strings.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	resp, _ := app.Test(req)
	assert.Equal(t, 200, resp.StatusCode)
}

func TestGetByUserID(t *testing.T) {
	app := fiber.New()
	mockService := &MockProfessionalProfileService{
		GetByUserIDFunc: func(userID uint) (*models.ProfessionalProfile, error) {
			return &models.ProfessionalProfile{
				Model:    gorm.Model{ID: 10},
				UserID:   userID,
				Bio:      "Bio",
				Category: models.CategoryNutritionist,
			}, nil
		},
	}
	handler := handlers.NewProfessionalProfileHandler(mockService)
	app.Get("/professional/profile/user/:user_id", handler.GetByUserID)

	req := httptest.NewRequest("GET", "/professional/profile/user/123", nil)
	resp, _ := app.Test(req)
	assert.Equal(t, 200, resp.StatusCode)
}

func TestGetByProfessionalID(t *testing.T) {
	app := fiber.New()
	mockService := &MockProfessionalProfileService{
		GetByProfessionalIDFunc: func(profileID uint) (*models.ProfessionalProfile, error) {
			return &models.ProfessionalProfile{
				Model:    gorm.Model{ID: profileID},
				UserID:   33,
				Bio:      "Bio",
				Category: models.CategoryNutritionist,
			}, nil
		},
	}
	handler := handlers.NewProfessionalProfileHandler(mockService)
	app.Get("/professional/profile/:id", handler.GetByProfessionalID)

	req := httptest.NewRequest("GET", "/professional/profile/55", nil)
	resp, _ := app.Test(req)
	assert.Equal(t, 200, resp.StatusCode)
}

func TestListProfessionals(t *testing.T) {
	app := fiber.New()
	mockService := &MockProfessionalProfileService{
		ListProfessionalsFunc: func(category, name string, tags []string, onlyOnline, onlyPresential *bool) ([]models.ProfessionalProfile, error) {
			return []models.ProfessionalProfile{
				{Model: gorm.Model{ID: 1}, Bio: "Bio1"},
				{Model: gorm.Model{ID: 2}, Bio: "Bio2"},
			}, nil
		},
	}
	handler := handlers.NewProfessionalProfileHandler(mockService)
	app.Get("/professional/list", handler.ListProfessionals)

	req := httptest.NewRequest("GET", "/professional/list?category=nutritionist&name=Ana", nil)
	resp, _ := app.Test(req)
	assert.Equal(t, 200, resp.StatusCode)
	var result []map[string]any
	json.NewDecoder(resp.Body).Decode(&result)
	assert.Len(t, result, 2)
}

func TestEditProfile(t *testing.T) {
	app := fiber.New()
	mockService := &MockProfessionalProfileService{
		EditProfileFunc: func(userID, profileID uint, data *models.ProfessionalProfile) error {
			return nil
		},
		GetByProfessionalIDFunc: func(profileID uint) (*models.ProfessionalProfile, error) {
			return &models.ProfessionalProfile{
				Model:    gorm.Model{ID: profileID},
				UserID:   33,
				Bio:      "BioAtualizada",
				Category: models.CategoryNutritionist,
			}, nil
		},
	}
	handler := handlers.NewProfessionalProfileHandler(mockService)
	app.Put("/professional/profile/:id", func(c *fiber.Ctx) error {
		c.Locals("user_id", uint(1))
		return handler.EditProfile(c)
	})

	body := `{"bio":"NovaBio"}`
	req := httptest.NewRequest("PUT", "/professional/profile/5", strings.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	resp, _ := app.Test(req)
	assert.Equal(t, 200, resp.StatusCode)
}

func TestDeleteProfile(t *testing.T) {
	app := fiber.New()
	mockService := &MockProfessionalProfileService{
		DeleteProfileFunc: func(userID, profileID uint) error {
			return nil
		},
	}
	handler := handlers.NewProfessionalProfileHandler(mockService)
	app.Delete("/professional/profile/:id", func(c *fiber.Ctx) error {
		c.Locals("user_id", uint(1))
		return handler.DeleteProfile(c)
	})

	req := httptest.NewRequest("DELETE", "/professional/profile/7", nil)
	resp, _ := app.Test(req)
	assert.Equal(t, 200, resp.StatusCode)
}

// [Tests de sucesso omitidos para focar nos de erro]

func TestCreateProfile_Error(t *testing.T) {
	app := fiber.New()
	mockService := &MockProfessionalProfileService{
		CreateProfileFunc: func(userID uint, profile *models.ProfessionalProfile) error {
			return errors.New("erro de criação")
		},
	}
	handler := handlers.NewProfessionalProfileHandler(mockService)
	app.Post("/professional/profile", func(c *fiber.Ctx) error {
		c.Locals("user_id", uint(1))
		return handler.CreateProfile(c)
	})

	body := `{"bio":"Test Bio","category":"nutritionist","services":"A,B,C"}`
	req := httptest.NewRequest("POST", "/professional/profile", strings.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	resp, _ := app.Test(req)
	assert.Equal(t, 400, resp.StatusCode)
	var respBody map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&respBody)
	assert.Contains(t, respBody["error"], "erro de criação")
}

func TestCreateProfile_BadRequest(t *testing.T) {
	app := fiber.New()
	mockService := &MockProfessionalProfileService{
		CreateProfileFunc: func(userID uint, profile *models.ProfessionalProfile) error {
			return nil
		},
	}
	handler := handlers.NewProfessionalProfileHandler(mockService)
	app.Post("/professional/profile", func(c *fiber.Ctx) error {
		c.Locals("user_id", uint(1))
		return handler.CreateProfile(c)
	})

	// JSON malformado
	body := `{"bio":"Test Bio"`
	req := httptest.NewRequest("POST", "/professional/profile", strings.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	resp, _ := app.Test(req)
	assert.Equal(t, 400, resp.StatusCode)
}

func TestGetByUserID_NotFound(t *testing.T) {
	app := fiber.New()
	mockService := &MockProfessionalProfileService{
		GetByUserIDFunc: func(userID uint) (*models.ProfessionalProfile, error) {
			return nil, errors.New("profile not found")
		},
	}
	handler := handlers.NewProfessionalProfileHandler(mockService)
	app.Get("/professional/profile/user/:user_id", handler.GetByUserID)

	req := httptest.NewRequest("GET", "/professional/profile/user/9999", nil)
	resp, _ := app.Test(req)
	assert.Equal(t, 404, resp.StatusCode)
	var respBody map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&respBody)
	assert.Contains(t, respBody["error"], "profile not found")
}

func TestGetByProfessionalID_NotFound(t *testing.T) {
	app := fiber.New()
	mockService := &MockProfessionalProfileService{
		GetByProfessionalIDFunc: func(profileID uint) (*models.ProfessionalProfile, error) {
			return nil, errors.New("profile not found")
		},
	}
	handler := handlers.NewProfessionalProfileHandler(mockService)
	app.Get("/professional/profile/:id", handler.GetByProfessionalID)

	req := httptest.NewRequest("GET", "/professional/profile/999", nil)
	resp, _ := app.Test(req)
	assert.Equal(t, 404, resp.StatusCode)
	var respBody map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&respBody)
	assert.Contains(t, respBody["error"], "profile not found")
}

func TestEditProfile_Forbidden(t *testing.T) {
	app := fiber.New()
	mockService := &MockProfessionalProfileService{
		EditProfileFunc: func(userID, profileID uint, data *models.ProfessionalProfile) error {
			return services.ErrNotProfileOwner
		},
		GetByProfessionalIDFunc: func(profileID uint) (*models.ProfessionalProfile, error) {
			return &models.ProfessionalProfile{Model: gorm.Model{ID: profileID}, Bio: "BioAtualizada"}, nil
		},
	}
	handler := handlers.NewProfessionalProfileHandler(mockService)
	app.Put("/professional/profile/:id", func(c *fiber.Ctx) error {
		c.Locals("user_id", uint(2))
		return handler.EditProfile(c)
	})

	body := `{"bio":"NovaBio"}`
	req := httptest.NewRequest("PUT", "/professional/profile/5", strings.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	resp, _ := app.Test(req)
	assert.Equal(t, 403, resp.StatusCode)
}

func TestEditProfile_BadRequest(t *testing.T) {
	app := fiber.New()
	mockService := &MockProfessionalProfileService{
		EditProfileFunc: func(userID, profileID uint, data *models.ProfessionalProfile) error {
			return errors.New("erro qualquer")
		},
		GetByProfessionalIDFunc: func(profileID uint) (*models.ProfessionalProfile, error) {
			return &models.ProfessionalProfile{Model: gorm.Model{ID: profileID}, Bio: "BioAtualizada"}, nil
		},
	}
	handler := handlers.NewProfessionalProfileHandler(mockService)
	app.Put("/professional/profile/:id", func(c *fiber.Ctx) error {
		c.Locals("user_id", uint(2))
		return handler.EditProfile(c)
	})

	body := `{"bio":"NovaBio"}`
	req := httptest.NewRequest("PUT", "/professional/profile/5", strings.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	resp, _ := app.Test(req)
	assert.Equal(t, 400, resp.StatusCode)
}

func TestEditProfile_BadJson(t *testing.T) {
	app := fiber.New()
	mockService := &MockProfessionalProfileService{
		EditProfileFunc: func(userID, profileID uint, data *models.ProfessionalProfile) error {
			return nil
		},
		GetByProfessionalIDFunc: func(profileID uint) (*models.ProfessionalProfile, error) {
			return &models.ProfessionalProfile{Model: gorm.Model{ID: profileID}, Bio: "BioAtualizada"}, nil
		},
	}
	handler := handlers.NewProfessionalProfileHandler(mockService)
	app.Put("/professional/profile/:id", func(c *fiber.Ctx) error {
		c.Locals("user_id", uint(1))
		return handler.EditProfile(c)
	})

	body := `{"bio":"NovaBio"` // JSON inválido
	req := httptest.NewRequest("PUT", "/professional/profile/5", strings.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	resp, _ := app.Test(req)
	assert.Equal(t, 400, resp.StatusCode)
}

func TestDeleteProfile_Forbidden(t *testing.T) {
	app := fiber.New()
	mockService := &MockProfessionalProfileService{
		DeleteProfileFunc: func(userID, profileID uint) error {
			return errors.New("unauthorized: not the profile owner")
		},
	}
	handler := handlers.NewProfessionalProfileHandler(mockService)
	app.Delete("/professional/profile/:id", func(c *fiber.Ctx) error {
		c.Locals("user_id", uint(2))
		return handler.DeleteProfile(c)
	})

	req := httptest.NewRequest("DELETE", "/professional/profile/7", nil)
	resp, _ := app.Test(req)
	assert.Equal(t, 400, resp.StatusCode)
}

func TestDeleteProfile_BadRequest(t *testing.T) {
	app := fiber.New()
	mockService := &MockProfessionalProfileService{
		DeleteProfileFunc: func(userID, profileID uint) error {
			return errors.New("delete error")
		},
	}
	handler := handlers.NewProfessionalProfileHandler(mockService)
	app.Delete("/professional/profile/:id", func(c *fiber.Ctx) error {
		c.Locals("user_id", uint(1))
		return handler.DeleteProfile(c)
	})

	req := httptest.NewRequest("DELETE", "/professional/profile/8", nil)
	resp, _ := app.Test(req)
	assert.Equal(t, 400, resp.StatusCode)
}
