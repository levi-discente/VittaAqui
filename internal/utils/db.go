package utils

import (
	"log"

	"github.com/levirenato/VittaAqui/internal/config"
	"github.com/levirenato/VittaAqui/internal/models"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

func ConnectDatabase(cfg config.Config) *gorm.DB {
	db, err := gorm.Open(postgres.Open(cfg.GetDSN()), &gorm.Config{})
	if err != nil {
		log.Fatal("Failed to connect to database: ", err)
	}

	db.AutoMigrate(&models.User{}, &models.ProfessionalProfile{}, &models.ProfileTag{})

	return db
}
