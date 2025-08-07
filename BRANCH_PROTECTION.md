# Branch Protection Rules

Este repositório deve ter as seguintes regras de proteção configuradas no branch `main`:

## Configuração no GitHub

1. Acesse o repositório: https://github.com/edufesta/totalsat-pdf-to-csv
2. Vá em **Settings** → **Branches**
3. Clique em **Add rule** ou **Add branch protection rule**
4. Configure:

### Branch name pattern
```
main
```

### Proteções Recomendadas
- ✅ **Restrict pushes that create files larger than 100 MB**
- ✅ **Require a pull request before merging**
  - ✅ Require approvals: 1
  - ✅ Dismiss stale reviews when new commits are pushed
  - ✅ Require review from code owners
- ✅ **Require status checks to pass before merging**
- ✅ **Require branches to be up to date before merging**
- ✅ **Require conversation resolution before merging**
- ✅ **Restrict pushes that create files larger than specified limit**

### Restrições de Push
- ✅ **Restrict push access to specific people or teams**
  - Adicionar: `edufesta` (seu usuário GitHub)
  - Permitir force pushes apenas para administradores

### Regras para Administradores
- ⚠️ **Include administrators** (opcional - aplicar regras também para admins)
- ✅ **Allow force pushes** (apenas para você como admin)
- ✅ **Allow deletions** (apenas para você como admin)

## Configuração Local

Para trabalhar com essas proteções:

### Workflow recomendado
```bash
# 1. Criar branch para mudanças
git checkout -b feature/nova-funcionalidade

# 2. Fazer commits na branch
git add .
git commit -m "Sua mensagem"
git push origin feature/nova-funcionalidade

# 3. Criar Pull Request no GitHub
# 4. Após aprovação, fazer merge via GitHub
```

### Bypass para o proprietário (você)
Se configurado corretamente, você ainda poderá:
```bash
# Push direto no main (apenas você)
git push origin main

# Force push se necessário (apenas você)
git push --force origin main
```

## Usuários Permitidos
- `edufesta` (proprietário) - acesso total
- Outros usuários - devem usar Pull Requests

## Benefícios
- 🔒 Protege o branch principal de alterações acidentais
- 📝 Força documentação via Pull Requests
- 🔍 Permite revisão de código antes do merge
- 📊 Mantém histórico limpo e auditável
- ⚡ Você mantém acesso direto como proprietário
