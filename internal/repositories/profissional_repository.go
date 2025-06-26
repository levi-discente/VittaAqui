package repositories

import (
	"github.com/levirenato/VittaAqui/internal/models"

	"gorm.io/gorm"
)

type ProfessionalProfileRepository struct {
	db *gorm.DB
}

func NewProfessionalProfileRepository(db *gorm.DB) *ProfessionalProfileRepository {
	return &ProfessionalProfileRepository{db}
}

func (r *ProfessionalProfileRepository) Create(profile *models.ProfessionalProfile) error {
	return r.db.Create(profile).Error
}

func (r *ProfessionalProfileRepository) GetByUserID(userID uint) (*models.ProfessionalProfile, error) {
	var profile models.ProfessionalProfile
	err := r.db.Preload("Tags").Where("user_id = ?", userID).First(&profile).Error
	return &profile, err
}

func (r *ProfessionalProfileRepository) GetByProfessionalID(profileID uint) (*models.ProfessionalProfile, error) {
	var profile models.ProfessionalProfile
	err := r.db.Preload("Tags").First(&profile, profileID).Error
	return &profile, err
}

func (r *ProfessionalProfileRepository) ListProfessionals(category, name string, tags []string, onlyOnline, onlyPresential *bool) ([]models.ProfessionalProfile, error) {
	var profiles []models.ProfessionalProfile
	tx := r.db.Model(&models.ProfessionalProfile{}).Preload("Tags")

	if category != "" {
		tx = tx.Where("category = ?", category)
	}
	if name != "" {
		tx = tx.Joins("JOIN users ON users.id = professional_profiles.user_id").
			Where("users.name ILIKE ?", "%"+name+"%")
	}
	if onlyOnline != nil {
		tx = tx.Where("only_online = ?", *onlyOnline)
	}
	if onlyPresential != nil {
		tx = tx.Where("only_presential = ?", *onlyPresential)
	}
	if len(tags) > 0 {
		tx = tx.Joins("JOIN profile_tags ON profile_tags.profile_id = professional_profiles.id").
			Where("profile_tags.name IN ?", tags)
	}

	tx = tx.Distinct()

	err := tx.Find(&profiles).Error
	return profiles, err
}

// Edit atualiza um perfil profissional
func (r *ProfessionalProfileRepository) Edit(profile *models.ProfessionalProfile) error {
	// Atualiza o perfil
	err := r.db.Session(&gorm.Session{FullSaveAssociations: true}).Save(profile).Error
	return err
}

func (r *ProfessionalProfileRepository) Delete(profileID uint) error {
	r.db.Where("profile_id = ?", profileID).Delete(&models.ProfileTag{})
	return r.db.Delete(&models.ProfessionalProfile{}, profileID).Error
}
