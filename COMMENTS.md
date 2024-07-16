# Decisão da arquitetura utilizada
No início, optei por usar opções que rodavam localmente na máquina para indexação e geração de texto para o usuário. Entretanto, tive muitos obstáculos no meio do caminho e, devido ao tempo curto, parti para soluções on-line que cobram por uso (OpenAI).

Assim, utilizei ao máximo bibliotecas que rodassem localmente e, na geração e embedding do texto, optei pelas soluções prontas da OpenAI.

Utilizei soluções da LangChain para indexação e gerenciamento de geração de texto. Também optei por bibliotecas já conhecidas por mim (StreamLit) para criação do aplicativo (interface do usuário) e processamento de texto e pdf.

Na parte de vídeo, utilizei recursos que rodam localmente para fazer download e tratamento do vídeo para áudio. Já na parte da transcrição do áudio para texto, optei por soluções da OpenAI também devido a acurácia e eficiência - nesta etapa as soluções da OpenAI rodam localmente e gratuitamente.

Após o tratamento dos dados, a próxima etapa foi a indexação dos mesmos através das soluções da LangChain. Criado esse index, fora utilizado o conhecido ChatGPT para geração de texto baseado no contexto dos dados.

# Lista de bibliotecas de terceiros utilizadas
```
PyMuPDF==1.24.7

langchain==0.2.8

langchain_community==0.2.7

langchain_openai==0.1.16

moviepy==1.0.3

numpy<2.0.0

faiss-cpu==1.7.4

openai==1.35.14

openai_whisper==20231117

pydub==0.25.1

python-dotenv==1.0.1

Requests==2.32.3

scikit_learn==1.4.1.post1

streamlit==1.36.0

tiktoken==0.7.0
```

# O que você melhoraria se tivesse mais tempo
Acrescentaria um módulo para detectar as dificuldades do usuário para gerar texto, áudio ou vídeo de modo a melhorar o aprendizado. Devido ao tempo perdido buscando soluções open-source que rodassem localmente, não tive tempo hábil para procurar soluções para este problema.

Entretanto, busquei sempre mostrar em qual documento e em qual página/minuto a informação que o usuário solicitou foi buscada.

# Quais requisitos obrigatórios que não foram entregues
**Todos requisitos obrigatórios** foram entregues. O único diferencial que faltou, como dito anteriormente, foi:
*Avaliação da capacidade do sistema em identificar corretamente as dificuldades dos usuários e adaptar o conteúdo de aprendizagem conforme necessário.*