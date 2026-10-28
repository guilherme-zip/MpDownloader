# MpDownloader

Aplicação de terminal interativa, escrita em Python, que baixa vídeos do YouTube como **MP3** ou **MP4** . Você escolhe a qualidade do áudio, o nome do arquivo e a pasta de destino, tudo por meio de menus simples.

## Funcionalidades

- Download de áudio convertido para **MP3** com qualidade configurável (128, 192, 256 ou 320 kbps)
- Download de vídeo no formato **MP4**
- Exibição de título, canal e duração do vídeo antes de baixar
- Nome do arquivo personalizável (padrão: título do vídeo)
- Pasta de destino personalizável (padrão: `downloads`), criada automaticamente se não existir
- Resumo e dupla confirmação antes de iniciar o download
- Tratamento de erros (URL inválida, vídeo privado, falta de conexão etc.) sem encerrar o programa

## Requisitos

- **Python 3.8+**
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** 
>>> pip install yt-dlp

- **[FFmpeg](https://ffmpeg.org/download.html)**, instalado e disponível no `PATH`. 
>>> Ele é necessário para converter o áudio em MP3 e para mesclar vídeo e áudio no MP4

## Instalação

1. Clone o repositório ou baixe o arquivo do script:

   ```bash
   git clone <url-do-repositorio>
   cd <pasta-do-projeto>
   ```

2. Instale o `yt-dlp`:

   ```bash
   pip install yt-dlp
   ```

3. Instale o FFmpeg de acordo com o seu sistema:

   | Sistema | Comando |
   |---------|---------|
   | Windows (winget) | `winget install ffmpeg` |
   | Windows (Chocolatey) | `choco install ffmpeg` |
   | macOS (Homebrew) | `brew install ffmpeg` |
   | Ubuntu/Debian | `sudo apt install ffmpeg` |

4. Confirme que o FFmpeg está acessível:

   ```bash
   ffmpeg -version
   ```

## Como usar

Execute o script:

```bash
python youtube_mp3_downloader.py
```

### Fluxo do programa

1. **Menu principal**: escolha entre baixar MP3, baixar MP4 ou sair.
2. **URL**: cole o link do vídeo do YouTube.
3. **Informações**: o programa mostra título, canal e duração, e pede confirmação.
4. **Configurações**:
   - qualidade do áudio (apenas para MP3);
   - nome do arquivo (ENTER usa o título do vídeo);
   - pasta de destino (ENTER usa `downloads`).
5. **Resumo**: confira os dados e confirme para iniciar.
6. **Download**: o arquivo é baixado, convertido (se MP3) e salvo na pasta escolhida.

### Exemplo de sessão

```text
==================================================
        YOUTUBE → MP3 DOWNLOADER
==================================================

1 - Baixar áudio como MP3
2 - Baixar vídeo como MP4
3 - Sair

Escolha uma opção: 1

Cole a URL do YouTube:
> https://www.youtube.com/watch?v=XXXXXXXXXXX

Informações encontradas:
--------------------------------------------------
Título : Exemplo de vídeo
Canal  : Canal de exemplo
Duração: 3:45
--------------------------------------------------

Deseja continuar? [S/N]: s

Escolha a qualidade do áudio:
1 - 128 kbps
2 - 192 kbps
3 - 256 kbps
4 - 320 kbps

Digite uma opção: 4
```

## Opções de qualidade (MP3)

| Opção | Bitrate |
|:-----:|:-------:|
| 1 | 128 kbps |
| 2 | 192 kbps |
| 3 | 256 kbps |
| 4 | 320 kbps |

> A qualidade final depende do áudio original disponibilizado pelo YouTube. Escolher um bitrate maior não melhora uma fonte de qualidade inferior.

## Estrutura do código

| Função | Descrição |
|--------|-----------|
| `limpar_tela()` | Limpa o terminal (`cls` no Windows, `clear` em Linux/macOS) |
| `mostrar_cabecalho()` | Exibe o título da aplicação |
| `obter_informacoes(url)` | Extrai os metadados do vídeo sem baixá-lo |
| `escolher_qualidade()` | Pergunta o bitrate do MP3 e valida a entrada |
| `baixar_mp3(...)` | Baixa o melhor áudio e converte para MP3 via FFmpeg |
| `baixar_video_mp4(...)` | Baixa o melhor vídeo e áudio e salva como MP4 |
| `sistema()` | Loop principal com o menu e todo o fluxo de interação |

## Solução de problemas

- **`ffmpeg not found` / `ffprobe not found`**: o FFmpeg não está instalado ou não está no `PATH`. Reinstale e abra um novo terminal.
- **Erro ao obter informações**: verifique a URL, a conexão com a internet e se o vídeo não é privado ou restrito por região ou idade.
- **Downloads falhando de repente**: o YouTube muda com frequência. Atualize o yt-dlp com `pip install -U yt-dlp`.
- **Erro ao salvar o arquivo**: evite caracteres inválidos no nome, como `\ / : * ? " < > |`, e confirme que você tem permissão de escrita na pasta de destino.

