#!/usr/bin/env python3
"""
Script de teste rápido do Mangaba AI - Setup Verification
Verifica se o ambiente está funcionando corretamente
"""

import os
import sys
from pathlib import Path

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def print_success(text):
    print(f"  ✅ {text}")

def print_error(text):
    print(f"  ❌ {text}")

def print_warning(text):
    print(f"  ⚠️  {text}")

def print_info(text):
    print(f"  ℹ️  {text}")

def main():
    print_header("MANGABA AI - VERIFICAÇÃO DE SETUP")
    
    # 1. Verificar estrutura do projeto
    print("\n📁 Verificando estrutura do projeto...")
    
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    required_files = [
        "mangaba_agent.py",
        "config.py",
        ".env",
        "pyproject.toml",
        "README.md",
    ]
    
    required_dirs = [
        "protocols",
        "scripts",
        "examples",
        "docs",
    ]
    
    all_ok = True
    
    for file in required_files:
        if (project_root / file).exists():
            print_success(f"Arquivo encontrado: {file}")
        else:
            print_error(f"Arquivo não encontrado: {file}")
            all_ok = False
    
    for dir_name in required_dirs:
        if (project_root / dir_name).exists():
            print_success(f"Diretório encontrado: {dir_name}/")
        else:
            print_error(f"Diretório não encontrado: {dir_name}/")
            all_ok = False
    
    # 2. Verificar Python
    print("\n🐍 Verificando Python...")
    print_success(f"Versão Python: {sys.version.split()[0]}")
    print_success(f"Executável: {sys.executable}")
    
    # 3. Verificar dependências
    print("\n📦 Verificando dependências...")
    
    required_packages = [
        "google.generativeai",
        "dotenv",
        "loguru",
        "pydantic",
        "requests",
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print_success(f"Módulo importado: {package}")
        except ImportError:
            print_error(f"Módulo não encontrado: {package}")
            all_ok = False
    
    # 4. Verificar .env
    print("\n🔐 Verificando configuração (.env)...")
    
    env_file = project_root / ".env"
    if env_file.exists():
        print_success("Arquivo .env encontrado")
        
        # Carregar .env
        from dotenv import load_dotenv
        load_dotenv(env_file)
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key and api_key.strip():
            print_success("GOOGLE_API_KEY configurada")
        else:
            print_warning("GOOGLE_API_KEY vazia - Configure antes de usar!")
        
        # Verificar outras variáveis
        model = os.getenv("MODEL_NAME", "não definido")
        print_info(f"MODEL_NAME: {model}")
        
        log_level = os.getenv("LOG_LEVEL", "não definido")
        print_info(f"LOG_LEVEL: {log_level}")
    else:
        print_error("Arquivo .env não encontrado!")
        all_ok = False
    
    # 5. Verificar se pode importar o agente
    print("\n🤖 Verificando importação do agente...")
    
    try:
        from mangaba_agent import MangabaAgent
        print_success("MangabaAgent importado com sucesso!")
        
        # Tentar criar uma instância (sem conectar à API)
        print_info("Testando criação de instância...")
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key or not api_key.strip():
            print_warning("GOOGLE_API_KEY não configurada - usando chave de teste (não conectará)")
            test_key = "test-key-not-real"
        else:
            test_key = api_key
        
        try:
            agent = MangabaAgent(api_key=test_key)
            print_success(f"Agente criado: {agent.agent_id}")
            print_success(f"Modelo: {agent.model_name}")
        except Exception as e:
            # É esperado falhar sem uma chave real
            if "GOOGLE_API_KEY" in str(e) or "api_key" in str(e).lower():
                print_warning(f"Erro esperado (chave não configurada): {str(e)[:60]}...")
            else:
                print_error(f"Erro ao criar agente: {e}")
                all_ok = False
    
    except ImportError as e:
        print_error(f"Erro ao importar MangabaAgent: {e}")
        all_ok = False
    
    # Resumo
    print_header("RESUMO")
    
    if all_ok:
        print_success("✅ SETUP OK - Ambiente pronto!")
        print_info("Próximo passo: Adicione sua GOOGLE_API_KEY ao arquivo .env")
        print_info("Depois: python examples/basic_example.py")
        return 0
    else:
        print_error("❌ Problemas encontrados - Veja acima")
        print_info("Resolva os erros e tente novamente")
        return 1

if __name__ == "__main__":
    sys.exit(main())
