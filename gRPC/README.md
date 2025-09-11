
1 - Montar o .proto definindo os dados de entrada e saída e o serviço.
2 - Gerar os stubs python : python -m grpc_tools.protoc -I'diretorio' --python_out='diretorio' --grpc_python_out='diretorio' 'filename'.proto
3 - Implementa a classe Multply para chamar scalarMultiply de Utils e retornar um resultado correto ou erro.
4 - Do lado do cliente impementar 


# Projeto Matrix gRPC


## Etapas de Configuração

1. **Montar o arquivo `.proto`**  
   - Montar o .proto definindo os dados de entrada e saída e o serviço.

2. **Gerar stubs Python**  
   - Utilize `grpc_tools.protoc` para gerar os arquivos de mensagens e stubs do serviço.  

3. **Implementar o servidor**  
   - Crie uma classe que implementa o serviço definido no `.proto`.  
   - O servidor recebe requisições de forma síncrona e processa uma tarefa por vez.

4. **Implementar o cliente**  
   - Conecte-se ao servidor usando um canal gRPC.  
   - Envie as requisições e trate as respostas retornadas pelo servidor.

5. **Fluxo de execução**  
   - Rodar o servidor nos PCs que atuarão como workers.  
   - O Master envia tarefas para cada worker e espera a resposta `"ok"` antes de enviar a próxima tarefa.  
   - Para grandes datasets, considere enviar os dados em chunks ou salvar checkpoints no disco.




