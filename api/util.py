import csv
import pandas as pd
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def gerarConsulta(nivel, depto, ano, periodo, listaTurmasColetadas):
    servico = Service(ChromeDriverManager().install())
    opcoes = webdriver.ChromeOptions()
    opcoes.add_experimental_option('excludeSwitches', ['enable-logging'])
    navegador = webdriver.Chrome(service=servico, options=opcoes)
    url = 'https://sigaa.unb.br/sigaa/public/turmas/listar.jsf?aba=p-ensino'
    navegador.get(url)
 
    navegador.find_element(By.NAME, 'formTurma:inputNivel').send_keys(nivel)
    navegador.find_element(By.NAME, 'formTurma:inputDepto').send_keys(depto)
    navegador.find_element(By.NAME, 'formTurma:inputAno').clear()
    navegador.find_element(By.NAME, 'formTurma:inputAno').send_keys(ano)
    navegador.find_element(By.NAME, 'formTurma:inputPeriodo').send_keys(periodo)
    navegador.find_element(By.NAME, 'formTurma:j_id_jsp_1370969402_11').click()

    time.sleep(2)
    coletarTurmas(navegador, listaTurmasColetadas)
    navegador.quit()
    return listaTurmasColetadas

def coletarTurmas(navegador, listaTurmasColetadas):
    listaTodosElementosDaPagina = navegador.find_elements(By.XPATH, '//*[@id="turmasAbertas"]/table/tbody/tr')
    listaCodigoTurma = navegador.find_elements(By.CLASS_NAME, "turma")
    listaProfCargaHor = navegador.find_elements(By.CLASS_NAME, "nome")
    listaAnoSemestre = navegador.find_elements(By.CLASS_NAME, "anoPeriodo")
    listaHorario = (navegador.find_elements(By.XPATH, "//*[@id='turmasAbertas']/table/tbody/tr//td[4]"))
    listaVagasOfertadas = navegador.find_elements(By.XPATH, '//*[@id="turmasAbertas"]/table/tbody/tr/td[6]')
    listaVagasOcupadas = navegador.find_elements(By.XPATH, '//*[@id="turmasAbertas"]/table/tbody/tr/td[7]')
    listaLocal = (navegador.find_elements(By.XPATH, "//*[@id='turmasAbertas']/table/tbody/tr//td[8]"))

    indLinhaAcumulada = 0
    indCabecalhoAtual = 0
    
    for linhaAtual in listaTodosElementosDaPagina:
        if linhaAtual.get_attribute("class") == 'agrupador':
            linhaCabecalho = linhaAtual.find_elements(By.XPATH, "//span[@class='tituloDisciplina']")[indCabecalhoAtual]
            codigoNomeMateria = linhaCabecalho.get_attribute('innerHTML')
            indCabecalhoAtual += 1
        if linhaAtual.get_attribute("class") == 'linhaPar' or linhaAtual.get_attribute("class") == 'linhaImpar':
            local = listaLocal[indLinhaAcumulada].get_attribute('innerText').strip()
            profCargaHor = listaProfCargaHor[indLinhaAcumulada].get_attribute('innerHTML')
            profCargaHor = profCargaHor.strip().split(" (")
            professor, cargahoraria = profCargaHor[0], profCargaHor[1][:3]
            codigoTurma = listaCodigoTurma[indLinhaAcumulada].get_attribute('innerHTML')
            anoSemestre = listaAnoSemestre[indLinhaAcumulada].get_attribute('innerHTML')
            ano, semestre = anoSemestre.split(".")
            horario = listaHorario[indLinhaAcumulada].get_attribute('innerText').strip()
            vagasOfertadas = listaVagasOfertadas[indLinhaAcumulada].get_attribute('innerHTML')
            vagasOcupadas = listaVagasOcupadas[indLinhaAcumulada].get_attribute('innerHTML')
            listaTurmasColetadas.append([codigoNomeMateria, professor, horario])
            indLinhaAcumulada += 1
    return listaTurmasColetadas

listaTurmasColetadas = []
gerarConsulta('GRADUAÇÃO', 'FACULDADE DO GAMA - BRASÍLIA', '2023', '2', listaTurmasColetadas)

with open("turmas.txt", 'a') as file:
    for item in listaTurmasColetadas:
        file.write("%s\n" % ",".join(item))