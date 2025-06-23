package utils

import (
	"encoding/json"
	"fmt"
	"net/http"
	"regexp"
)

type Address struct {
	CEP        string `json:"cep"`
	Logradouro string `json:"logradouro"`
	Bairro     string `json:"bairro"`
	Localidade string `json:"localidade"`
	UF         string `json:"uf"`
}

func LookupCEP(rawCEP string) (*Address, error) {
	cep := regexp.MustCompile(`\D`).ReplaceAllString(rawCEP, "")
	if len(cep) != 8 {
		return nil, fmt.Errorf("invalid CEP format")
	}

	url := fmt.Sprintf("https://viacep.com.br/ws/%s/json/", cep)
	res, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer res.Body.Close()

	if res.StatusCode != 200 {
		return nil, fmt.Errorf("failed to fetch CEP: HTTP %d", res.StatusCode)
	}

	var data map[string]any
	if err := json.NewDecoder(res.Body).Decode(&data); err != nil {
		return nil, err
	}
	if data["erro"] == true {
		return nil, fmt.Errorf("CEP not found")
	}

	addr := &Address{
		CEP:        data["cep"].(string),
		Logradouro: data["logradouro"].(string),
		Bairro:     data["bairro"].(string),
		Localidade: data["localidade"].(string),
		UF:         data["uf"].(string),
	}
	return addr, nil
}
