# Resolução de Problemas: Terminal Travado em Heredoc

**Gatilho:** Quando o processo de criação de arquivos via terminal (`cat <<EOF`) falha ou o terminal exibe prompts inesperados como `heredoc>`.

**Causa:**
Isso ocorre quando o comando `EOF` (delimitador) não é enviado corretamente ao final da stream de input, ou há conflitos de formatação no comando passado para a ferramenta `run_in_terminal`.

**Ação Corretiva (Memória):**
1.  **Diagnóstico:** Se o terminal retornar `heredoc>` e não finalizar.
2.  **Sinal de Interrupção (Control+C):** Na interface do VS Code ou terminal real, o usuário usaria `Ctrl+C`. Para o agente, isso significa interromper o comando atual ou encerrar o processo pendente (`pkill cat` ou similar se não puder enviar keystrokes) para liberar o lock do arquivo.
3.  **Prevenção:** Ao escrever arquivos complexos com múltiplas linhas ou caracteres especiais, preferir utilizar a ferramenta `create_file` ou `edit_file` diretamente em vez de pipe via terminal (`cat > file`).

**Nota do Usuário:**
"fazer um control+c para finalizar o editor" quando estiver travado.