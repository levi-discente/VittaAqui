package utils

import (
	"github.com/klassmann/cpfcnpj"
)

func IsValidCPF(rawCPF string) bool {
	cleaned := cpfcnpj.Clean(rawCPF)
	return cpfcnpj.ValidateCPF(cleaned)
}

func IsValidCNPJ(rawCNPJ string) bool {
	cleaned := cpfcnpj.Clean(rawCNPJ)
	return cpfcnpj.ValidateCNPJ(cleaned)
}
