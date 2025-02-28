import json
import openai
import os


# Carregar o arquivo JSON original
def load_ui(file_path):
    if not os.path.exists(file_path):
        print(f"Erro: O arquivo {file_path} não foi encontrado.")
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Erro: O arquivo {file_path} não contém um JSON válido.")
        return None


# Salvar o novo layout otimizado
def save_ui(data, output_path):
    try:
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        print(f"Novo layout otimizado salvo em {output_path}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")


# Aplicar heurísticas básicas para melhoria do layout em todas as telas
def apply_heuristics(ui_data):
    grid_x = 20  # Margem horizontal inicial
    grid_y = 20  # Margem vertical inicial
    padding_x = 10  # Espaço entre elementos horizontalmente
    padding_y = 10  # Espaço entre elementos verticalmente

    if "screens" not in ui_data:
        print("Erro: Nenhuma tela encontrada no JSON.")
        return ui_data

    for screen in ui_data["screens"]:
        max_width = ui_data.get("ihm", {}).get("width", 800)  # Largura total da tela (padrão: 800px)
        components = screen.get("childs", [])

        # Ordenar os componentes por tipo para uma distribuição mais lógica
        components.sort(key=lambda c: c.get("typeComponent", ""))

        new_layout = []
        current_x, current_y = grid_x, grid_y
        row_height = 0  # Para manter alinhamento na linha

        for comp in components:
            width = comp.get("width", 100)
            height = comp.get("height", 50)

            # Verifica se cabe na linha atual, senão pula para a próxima linha
            if current_x + width > max_width:
                current_x = grid_x  # Reinicia X
                current_y += row_height + padding_y  # Pula para a próxima linha
                row_height = 0  # Reinicia a altura máxima da linha

            # Atualiza a posição do componente
            comp["posX"] = current_x
            comp["posY"] = current_y

            # Atualiza coordenadas para o próximo item
            current_x += width + padding_x
            row_height = max(row_height, height)  # Atualiza a altura da linha

            new_layout.append(comp)

        screen["childs"] = new_layout
    
    return ui_data


# Integração com o OpenAI GPT para melhorias avançadas
def enhance_with_gpt(ui_data, api_key):
    client = openai.OpenAI(api_key=api_key)

    prompt = {
        "layout": ui_data,
        "objective": "Otimizar layout para melhor usabilidade e estética",
        "guidelines": [
            "Melhorar distribuição dos espaços",
            "Garantir acessibilidade",
            "Usar princípios de design responsivo"
        ]
    }

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um especialista em design de UI/UX."},
                {"role": "user", "content": json.dumps(prompt)}
            ]
        )

        gpt_suggestions = json.loads(response.choices[0].message.content)
        return gpt_suggestions

    except Exception as e:
        print(f"Erro ao conectar com o GPT: {e}")
        return ui_data  # Retorna o layout original caso ocorra erro


# Pipeline completo de otimização do layout
def optimize_ui(file_path, output_path, api_key):
    ui_data = load_ui(file_path)
    if not ui_data:
        return

    ui_data = apply_heuristics(ui_data)
    ui_data = enhance_with_gpt(ui_data, api_key)
    save_ui(ui_data, output_path)


# Execução principal
if __name__ == "__main__":
    input_file = "C:/Users/carol/OneDrive/Documentos/Inova/GPTteste2/ide-manifest.json"  # Caminho atualizado
    output_file = "C:/Users/carol/OneDrive/Documentos/Inova/GPTteste2/forno2.json"  # Caminho atualizado

    # Substituir a chave API por variável de ambiente para segurança
    openai_api_key = os.getenv("OPENAI_API_KEY", "chave-falsa")  # Use a variável de ambiente

    optimize_ui(input_file, output_file, openai_api_key)
