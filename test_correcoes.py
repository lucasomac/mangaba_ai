#!/usr/bin/env python3
"""
Teste das correções dos 13 problemas identificados
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Testa se todos os imports funcionam"""
    print("📦 Testando imports...")
    try:
        from mangaba_agent import MangabaAgent
        from protocols.a2a import A2AAgent, A2AMessage, MessageType, A2AProtocol
        from protocols.mcp import MCPProtocol, MCPContext, ContextType, ContextPriority
        print("  ✅ Todos os imports OK")
        return True
    except Exception as e:
        print(f"  ❌ Erro no import: {e}")
        return False

def test_no_duplicate_methods():
    """Testa se métodos duplicados foram removidos"""
    print("\n🔍 Testando remoção de duplicatas...")
    try:
        from mangaba_agent import MangabaAgent
        import inspect
        
        # Verifica se analyze_text existe e tem implementação MCP
        source = inspect.getsource(MangabaAgent.analyze_text)
        
        # Deve ter MCP (not just call self.chat)
        if "self.mcp" in source and "analysis_context" in source:
            print("  ✅ analyze_text: Versão MCP completa mantida")
        else:
            print("  ⚠️  analyze_text: Versão simplificada (esperada versão MCP)")
            return False
            
        # Verifica se translate existe e tem implementação MCP
        source = inspect.getsource(MangabaAgent.translate)
        if "self.mcp" in source and "translation_context" in source:
            print("  ✅ translate: Versão MCP completa mantida")
        else:
            print("  ⚠️  translate: Versão simplificada (esperada versão MCP)")
            return False
            
        return True
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        return False

def test_thread_safety():
    """Testa se locks foram adicionados"""
    print("\n🔒 Testando thread-safety...")
    try:
        from protocols.a2a import A2AProtocol
        from protocols.mcp import MCPProtocol
        
        # Verifica se A2AProtocol tem lock
        a2a = A2AProtocol("test_agent")
        if hasattr(a2a, '_lock'):
            print("  ✅ A2AProtocol: Lock adicionado")
        else:
            print("  ⚠️  A2AProtocol: Lock não encontrado")
            return False
            
        # Verifica se MCPProtocol tem lock
        mcp = MCPProtocol()
        if hasattr(mcp, '_lock'):
            print("  ✅ MCPProtocol: Lock adicionado")
        else:
            print("  ⚠️  MCPProtocol: Lock não encontrado")
            return False
            
        return True
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        return False

def test_broadcast_filters():
    """Testa se broadcast aceita filtros por tags"""
    print("\n📢 Testando broadcast com filtros...")
    try:
        from protocols.a2a import A2AProtocol
        import inspect
        
        # Verifica assinatura do método broadcast
        sig = inspect.signature(A2AProtocol.broadcast)
        
        if 'target_tags' in sig.parameters:
            print("  ✅ broadcast: Parâmetro target_tags adicionado")
            return True
        else:
            print("  ⚠️  broadcast: Parâmetro target_tags não encontrado")
            return False
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        return False

def test_session_validation():
    """Testa se validação de session_id foi adicionada"""
    print("\n🎫 Testando validação de sessão MCP...")
    try:
        from mangaba_agent import MangabaAgent
        import os
        
        # Desabilita logging para teste
        os.environ['LOG_LEVEL'] = 'ERROR'
        
        # Cria agente (deve validar session)
        agent = MangabaAgent(enable_mcp=True)
        
        # Verifica se sessão foi criada
        if agent.mcp_enabled and agent.current_session_id:
            print(f"  ✅ Sessão MCP criada e validada: {agent.current_session_id[:16]}...")
            return True
        else:
            print("  ⚠️  Sessão MCP não validada corretamente")
            return False
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        return False

def test_error_flag_correction():
    """Testa se flag success foi corrigida para ação desconhecida"""
    print("\n🚩 Testando flag success em ação desconhecida...")
    try:
        from mangaba_agent import MangabaAgent
        from protocols.a2a import A2AMessage, MessageType
        import inspect
        
        # Verifica código do handler
        source = inspect.getsource(MangabaAgent.handle_mangaba_request)
        
        # Deve ter create_response com False para ação desconhecida
        if 'create_response(message, result, False)' in source or 'success=False' in source:
            print("  ✅ Flag success=False para ação desconhecida")
            return True
        else:
            print("  ⚠️  Flag success não corrigida")
            return False
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        return False

def test_no_hasattr_checks():
    """Testa se verificações hasattr desnecessárias foram removidas"""
    print("\n🔧 Testando remoção de hasattr desnecessários...")
    try:
        from mangaba_agent import MangabaAgent
        import inspect
        
        methods_to_check = [
            ('get_context_summary', 'get_session_contexts'),
            ('send_agent_request', 'create_request'),
            ('broadcast_message', 'broadcast')
        ]
        
        all_ok = True
        for method_name, target in methods_to_check:
            source = inspect.getsource(getattr(MangabaAgent, method_name))
            if f"hasattr(self.a2a_protocol, '{target}')" in source or \
               f"hasattr(self.mcp, '{target}')" in source:
                print(f"  ⚠️  {method_name}: hasattr ainda presente")
                all_ok = False
            else:
                print(f"  ✅ {method_name}: hasattr removido")
        
        return all_ok
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("="*70)
    print("  TESTE DAS CORREÇÕES - 13 PROBLEMAS")
    print("="*70)
    
    tests = [
        ("Imports", test_imports),
        ("Remoção de duplicatas", test_no_duplicate_methods),
        ("Thread-safety", test_thread_safety),
        ("Broadcast com filtros", test_broadcast_filters),
        ("Validação de sessão", test_session_validation),
        ("Flag success corrigida", test_error_flag_correction),
        ("Remoção de hasattr", test_no_hasattr_checks),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Erro ao executar teste '{name}': {e}")
            results.append((name, False))
    
    # Resumo
    print("\n" + "="*70)
    print("  RESUMO DOS TESTES")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"  {status}: {name}")
    
    print(f"\n  Total: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n  🎉 TODAS AS CORREÇÕES VALIDADAS COM SUCESSO!")
        return 0
    else:
        print(f"\n  ⚠️  {total - passed} correções precisam de atenção")
        return 1

if __name__ == "__main__":
    sys.exit(main())
