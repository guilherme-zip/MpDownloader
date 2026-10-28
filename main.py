"""
MpDownloader
========================

Aplicação de terminal interativa que baixa o áudio de vídeos do YouTube e o
converte para MP3, permitindo escolher a qualidade, o nome do arquivo e a
pasta de destino.

Dependências:
    - yt-dlp  (pip install yt-dlp)
    - FFmpeg  (precisa estar instalado e disponível no PATH, pois é usado
               pelo yt-dlp para converter o áudio em MP3)

Uso:
    python youtube_mp3_downloader.py

Fluxo do programa:
    1. Menu principal (baixar ou sair)
    2. Usuário informa a URL do vídeo
    3. O programa exibe título, canal e duração para confirmação
    4. Usuário escolhe qualidade, nome do arquivo e pasta de destino
    5. Resumo final e confirmação
    6. Download e conversão para MP3
"""

import os
from pathlib import Path

import yt_dlp


def limpar_tela():
    """Limpa o terminal.

    Usa o comando ``cls`` no Windows (``os.name == "nt"``) e ``clear`` nos
    demais sistemas (Linux e macOS).
    """
    os.system("cls" if os.name == "nt" else "clear")


def mostrar_cabecalho():
    """Exibe o cabeçalho (título) da aplicação no terminal."""
    print("=" * 50)
    print("        YOUTUBE → MP3 DOWNLOADER")
    print("=" * 50)
    print()


def obter_informacoes(url):
    """Obtém os metadados de um vídeo sem realizar o download.

    Args:
        url (str): URL do vídeo do YouTube.

    Returns:
        dict | None: Dicionário com as informações do vídeo (título, canal,
        duração etc.) ou ``None`` caso ocorra algum erro, como URL inválida,
        vídeo privado ou falta de conexão.
    """
    opcoes = {
        "quiet": True,        # Suprime a saída padrão do yt-dlp
        "no_warnings": True,  # Oculta avisos
    }

    try:
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            # download=False: apenas extrai os metadados
            informacoes = ydl.extract_info(url, download=False)

        return informacoes

    except Exception as erro:
        print(f"\nErro ao obter informações: {erro}")
        return None


def escolher_qualidade():
    """Solicita ao usuário a qualidade (bitrate) do MP3 resultante.

    Repete a pergunta até que uma opção válida (1 a 4) seja digitada.

    Returns:
        str: Bitrate em kbps, como texto (``"128"``, ``"192"``, ``"256"``
        ou ``"320"``), no formato esperado pelo ``preferredquality`` do
        yt-dlp.
    """
    print("\nEscolha a qualidade do áudio:")
    print("1 - 128 kbps")
    print("2 - 192 kbps")
    print("3 - 256 kbps")
    print("4 - 320 kbps")

    # Mapeia a opção do menu para o bitrate correspondente
    qualidades = {
        "1": "128",
        "2": "192",
        "3": "256",
        "4": "320",
    }

    while True:
        opcao = input("\nDigite uma opção: ").strip()

        if opcao in qualidades:
            return qualidades[opcao]

        print("Opção inválida. Escolha entre 1 e 4.")


def baixar_mp3(url, nome_arquivo, pasta, qualidade):
    """Baixa o áudio de um vídeo do YouTube e o converte para MP3.

    O melhor áudio disponível é baixado e, em seguida, convertido para MP3
    com o FFmpeg na qualidade escolhida. A pasta de destino é criada
    automaticamente caso não exista.

    Args:
        url (str): URL do vídeo do YouTube.
        nome_arquivo (str): Nome do arquivo de saída, sem a extensão.
        pasta (str): Caminho da pasta onde o arquivo será salvo.
        qualidade (str): Bitrate do MP3 em kbps (ex.: ``"192"``).

    Observação:
        Erros durante o processo são capturados e exibidos na tela, sem
        interromper a execução do programa.
    """
    pasta_saida = Path(pasta)

    try:
        # Cria a pasta (e as pastas-pai) se ainda não existir
        pasta_saida.mkdir(parents=True, exist_ok=True)

        # Modelo do caminho de saída. O yt-dlp substitui %(ext)s pela
        # extensão final do arquivo.
        caminho = pasta_saida / f"{nome_arquivo}.%(ext)s"

        opcoes = {
            "format": "bestaudio/best",  # Melhor qualidade de áudio disponível
            "outtmpl": str(caminho),     # Modelo do nome/caminho do arquivo
            "postprocessors": [
                {
                    # Extrai o áudio e converte para MP3 usando o FFmpeg
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": qualidade,
                }
            ],
        }

        print("\nIniciando download...")
        print("-" * 50)

        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.download([url])

        print("-" * 50)
        print("Download concluído!")
        print(f"Local: {pasta_saida.resolve()}")

    except Exception as erro:
        print("\nNão foi possível realizar o download.")
        print(f"Erro: {erro}")


def baixar_video_mp4(url, nome_arquivo, pasta):
    """Baixa o vídeo do YouTube e salva no formato MP4."""
    pasta_saida = Path(pasta)
    try:
        pasta_saida.mkdir(parents=True, exist_ok=True)
        caminho = pasta_saida / f"{nome_arquivo}.%(ext)s"
        opcoes = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "merge_output_format": "mp4",
            "outtmpl": str(caminho),
        }
        print("\nIniciando download do vídeo...")
        print("-" * 50)
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.download([url])
        print("-" * 50)
        print("Download concluído!")
        print(f"Local: {pasta_saida.resolve()}")
    except Exception as erro:
        print("\nNão foi possível realizar o download do vídeo.")
        print(f"Erro: {erro}")


def sistema():
    """Executa o loop principal da aplicação (menu interativo).

    Controla todo o fluxo de interação com o usuário: menu, leitura da URL,
    exibição das informações do vídeo, confirmações, escolha de qualidade,
    nome do arquivo e pasta de destino, e a chamada do download.

    O loop só termina quando o usuário escolhe a opção "Sair".
    """
    while True:

        limpar_tela()
        mostrar_cabecalho()

        # ----- Menu principal -----
        print("1 - Baixar áudio como MP3")
        print("2 - Baixar vídeo como MP4")
        print("3 - Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "3":
            print("\nPrograma encerrado.")
            break

        if opcao not in ("1", "2"):
            print("\nOpção inválida.")
            input("Pressione ENTER para continuar...")
            continue

        limpar_tela()
        mostrar_cabecalho()

        # ----- Entrada da URL -----
        url = input("Cole a URL do YouTube:\n> ").strip()

        if not url:
            print("\nURL não informada.")
            input("\nPressione ENTER para continuar...")
            continue

        # ----- Informações do vídeo -----
        print("\nObtendo informações do vídeo...")

        info = obter_informacoes(url)

        # Se não foi possível obter as informações, volta ao menu
        if info is None:
            input("\nPressione ENTER para continuar...")
            continue

        titulo = info.get("title", "Sem título")
        canal = info.get("uploader", "Desconhecido")
        duracao = info.get("duration")  # Em segundos (pode ser None, ex.: lives)

        print("\nInformações encontradas:")
        print("-" * 50)
        print(f"Título : {titulo}")
        print(f"Canal  : {canal}")

        if duracao:
            # Converte segundos para o formato M:SS
            minutos = duracao // 60
            segundos = duracao % 60
            print(f"Duração: {minutos}:{segundos:02d}")

        print("-" * 50)

        # ----- Primeira confirmação: o vídeo está correto? -----
        confirmar = input("\nDeseja continuar? [S/N]: ").strip().lower()

        if confirmar != "s":
            print("\nDownload cancelado.")
            input("Pressione ENTER para continuar...")
            continue

        # ----- Qualidade do áudio (somente para MP3) -----
        qualidade = escolher_qualidade() if opcao == "1" else None

        # ----- Nome do arquivo (padrão: título do vídeo) -----
        nome_padrao = titulo

        print("\nNome do arquivo:")
        nome = input(f"Pressione ENTER para usar '{nome_padrao}'\n> ").strip()

        if not nome:
            nome = nome_padrao

        # ----- Pasta de destino (padrão: ./downloads) -----
        print("\nPasta de destino:")
        pasta = input("Pressione ENTER para usar 'downloads'\n> ").strip()

        if not pasta:
            pasta = "downloads"

        # ----- Resumo antes de baixar -----
        print("\n" + "=" * 50)
        print("RESUMO DO DOWNLOAD")
        print("=" * 50)
        extensao = "mp3" if opcao == "1" else "mp4"
        print(f"Arquivo  : {nome}.{extensao}")
        if opcao == "1":
            print(f"Qualidade: {qualidade} kbps")
        print(f"Pasta    : {pasta}")
        print("=" * 50)

        # ----- Segunda confirmação: iniciar o download? -----
        confirmar = input("\nIniciar download? [S/N]: ").strip().lower()

        if confirmar == "s":
            if opcao == "1":
                baixar_mp3(
                    url=url,
                    nome_arquivo=nome,
                    pasta=pasta,
                    qualidade=qualidade
                )
            else:
                baixar_video_mp4(
                    url=url,
                    nome_arquivo=nome,
                    pasta=pasta
                )
        else:
            print("\nDownload cancelado.")

        input("\nPressione ENTER para voltar ao menu...")


# Ponto de entrada: só executa quando o arquivo é rodado diretamente
# (e não quando importado como módulo).
if __name__ == "__main__":
    sistema()
    