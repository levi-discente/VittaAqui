package utils

import (
	// necessário para o //go:embed
	_ "embed"
	"log"

	"github.com/levirenato/VittaAqui/internal/config"
	"github.com/levirenato/VittaAqui/internal/models"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

//go:embed init_professionals.sql
var seedSQL []byte

func ConnectDatabase(cfg config.Config) *gorm.DB {
	dsn := cfg.GetDSN()
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatal("Failed to connect to database: ", err)
	}

	if err := db.AutoMigrate(
		&models.User{},
		&models.ProfessionalProfile{},
		&models.ProfileTag{},
		&models.Appointment{},
	); err != nil {
		log.Fatal("Failed to AutoMigrate: ", err)
	}

	var cnt int64
	if err := db.Model(&models.User{}).Count(&cnt).Error; err != nil {
		log.Fatal("Failed to count users: ", err)
	}
	if cnt == 0 {
		if err := seedInitProfessionals(db); err != nil {
			log.Fatal("Failed to seed initial data: ", err)
		}
	}

	return db
}

func seedInitProfessionals(db *gorm.DB) error {
	// converte o []byte embarcado em string SQL
	sql := string(seedSQL)

	return db.Transaction(func(tx *gorm.DB) error {
		if err := tx.Exec(sql).Error; err != nil {
			return err
		}
		return nil
	})
}
