#================================IMPORTAÇÕES====================================
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify

#=================================CLASSES==========================================
from core.validacao_put import atualizar_prod,atualizar_cliente,atualizar_fornecedor,atualizar_pedido_fornecedor,atualizar_itens,atualizar_producao,atualizar_materiais,atualizar_pagamentos,atualizar_pedidocliente,atualizar_funcionarios,atualizar_item_pedido,atualizar_oque_vai ,extcep,extemail,extcnpj
from core.validacao_post import validar_cpf, validar_nome
from core.validator import Validar
from core.security import gerar_hash_senha

from models.clientes import Cliente
from models.fornecedor import Fornecedor
from models.pedido_fornecedor import PedidoFornecedor
from models.pedido_cliente import PedidoCliente
from models.funcionario import Funcionario
from models.produtos import Produto
from models.login import Login 
from models.materia_prima import Materia_prima
from models.producao import Producao


app= Flask(__name__)

app.secret_key = 'HeF#2026'

token = "22588|E5cNBvGnqJj0OK9M34HXFDVf4DauZ4J7"

def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

def to_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default




@app.route("/")
def index():
    if "id" in session:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


'''===================== LOGIN =========================='''



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Pega os valores enviados pelos atributos 'name' do formulário HTML
        email = request.form.get("email_funcionario")
        senha = request.form.get("senha_funcionario")
        
        # Chama a autenticação da sua classe Funcionario
        usuario = Funcionario.autenticar(email, senha)
        
        if usuario:
            # Salva na sessão (caso 'usuario' seja objeto, use usuario.id / usuario.nome_funcionario)
            session["id"] = usuario.id if hasattr(usuario, "id") else usuario["id"]
            session["nome_funcionario"] = usuario.nome_funcionario if hasattr(usuario, "nome_funcionario") else usuario["nome_funcionario"]
            
            flash("Login realizado com sucesso!", "success")
            # Redireciona o navegador para a rota /dashboard
            return redirect(url_for("dashboard"))

        # Caso login falhe:
        flash("E-mail ou senha inválidos.", "danger")

    return render_template("login.html")



    


'''====================================dashboard=========================================='''

'''@app.route("/dashboard")
def dashboard():
    =====produção=====
    prazo_cliente=get_ped_cliente_form(prazo_final_pedido_cliente)
    

    return render_template("dashboard.html")'''


@app.route("/inicio")
@app.route("/dashboard")
def dashboard():
    estoque_baixo = Materia_prima().count_itens()
    vendas_total = PedidoCliente().count()
    producao_total = Producao().count()
    pedidos_total = PedidoFornecedor().count()

    return render_template(
        "dashboard.html",
        estoque_baixo=estoque_baixo,
        vendas_total=vendas_total,
        producao_total=producao_total,
        pedidos_total=pedidos_total
    )

'''================================= MODELOS =================================================='''

@app.route("/modelos")
def modelos():
    return render_template("modelo.html")

'''=================================== ENTRADA================================================='''
@app.route("/entrada")
def entrada():
    return render_template("entrada.html")


'''================================== TRATAMENTO DE ERRO - 404====================================='''
@app.errorhandler(404)
def pag_nao_encontrada(error):
    return render_template("404.html"),404


'''===================================== HISTÓRICO DE COMPRA ========================================='''
@app.route("/compras", methods=["GET"])
def rend_hist_compra():
    return render_template("historico_compra.html")


'''==================================== HISTÓRICO DE VENDAS============================================'''
@app.route ("/vendas", methods=["GET"])
def rend_hist_vendas():
    return render_template("historico_vendas.html")
'''================================== PERFIL USUARIO ==============================================='''
@app.route("/perfil", methods = ["GET"])
def rend_perfil():
    return render_template("perfil_usuario.html")


'''---------PRODUTO--------'''


def get_produto_form():
    print("request",request.form) 
    return {
        "nome_produto": request.form.get("nome_produto", "").strip() .upper(),
        "dimensoes_produto": request.form.get("dimensoes_produto","").strip(),
        "imagem_produto": request.form.get("imagem_produto","").strip(),
        "minimo_produto": to_int(request.form.get("minimo_produto","")).strip(),
        "ativado_produto": to_int(request.form.get("ativado_produto",""))
    }

@app.route("/produto", methods=["GET"])
def produto():
    return render_template("cad_produto.html")



'''========================RASTREIO==========================='''
@app.route("/rastreio", methods=["GET"])
def rend_rastreio():
    return render_template("rastreio.html")

'''Get Produto'''
@app.route("/produto/<int:indice>", methods=["GET"])
def buscar_produto(indice):
    if 0 <= indice < len(livro):
        return jsonify(livro)
    return jsonify({"erro":"Fornecedor inexistente no sistema"}),404

'''Delete Produto'''
@app.route("/produto/<int:indice>", methods = ["DELETE"])
def deletar_produto(indice):
    if indice < len(livro):
        livro.pop(indice)
        return jsonify({"mensagem": "Produto removido com sucesso!"})
    return jsonify({"erro": "Produto não encontrado."}), 404

'''Post Produto'''
@app.route("/produto", methods=["POST"])
def produto_incluir():
    dados = get_produto_form()
    produto = Produto(**dados)
    try:
        produto.insert()
        flash("Produto cadastrado com sucesso.", "sucesso")
        return redirect(url_for("produto"))
    except Exception as e:
        flash(f"Erro ao cadastrar : {e}", "erro")
        return render_template("cad_produto.html")

'''Put Produto'''
@app.route("/produto/<int:indice>", methods=["PUT"])
def atualizar_cadliv(indice):
    if indice <= len(livro):
        dados = request.get_json()
        if validar_put(dados) !=None:
            atualizar_prod(indice, dados, livro)
            return jsonify({"mensagem": "Livro atualizado com sucesso!"})
    return jsonify ({"erro": "Livro não encontrado"}), 404

"""---------CLIENTES-----------"""


@app.route("/cliente")
def cliente():
    return render_template("cad_cliente.html")


def get_cliente_form():
    print("request",request.form) 
    return {
        "nome_cliente": request.form.get("nome_cliente", "").strip() .upper(),
        "cnpj_cliente": request.form.get("cnpj_cliente","").strip(),
        "email_cliente": request.form.get("email_cliente","").strip(),
        "tel_cliente": request.form.get("tel_cliente","").strip(),
        "cep_cliente": request.form.get("cep_cliente","").strip(),
        "ativado_cliente": to_int(request.form.get("ativado_cliente",""))
    }


@app.route("/cliente/pesquisa", methods=["GET"])
def procurar_cliente():
    return render_template("consulta_cliente.html")

@app.route("/consulta/cliente", methods=["GET"])
def consulta_cliente():
    return render_template("consulta_cliente.html", cliente=Cliente.find_all_cliente(order_by = "id"))

@app.route("/consulta/funcionario", methods=["GET"])
def consulta_funcionario():
    return render_template("consulta_funcionario.html")

@app.route("/consulta/fornecedor", methods=["GET"])
def consulta_fornecedor():
    return render_template("consulta_fornecedor.html")

@app.route("/consulta/produtos", methods=["GET"])
def consulta_produtos():
    return render_template("consulta_produtos.html", produtos=Produto.find_all(order_by="id"))

'''Delete Clientes'''
@app.route("/cliente/pesquisa/<int:indice>", methods = ["DELETE"])
def deletar_cliente(indice):
    try:
        Cliente.safe_delete_cliente(id)
        flash("Produto excluído com sucesso.", "sucesso")
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao excluir produto: {e}", "erro")
    return redirect(url_for("consulta_cliente"))

'''Post Clientes'''
@app.route("/cadastro/cliente", methods=["POST"])
def cliente_incluir():
    dados = get_cliente_form()
    cliente = Cliente(**dados)
    try:
        cliente.insert(0)
        flash("Cliente cadastrado com sucesso.", "success")
        return redirect(url_for("cliente"))
    except Exception as e:
        flash(f"Erro ao cadastrar cliente: {e}", "danger")
        return render_template("cad_cliente.html")

'''Put Clientes'''
@app.route("/cliente/<int:indice>", methods=["PUT"])
def atualizar_cadcli(indice):
    dados = get_cliente_form()
    clientes = Cliente(**dados)
    erros = clientes.validate()

    if erros:
        for erro in erros:
            flash(erro, "erro")
        dados["id"] = id
        return render_template("cad_cliente.html", clientes=dados)

    try:
        if not Cliente.find_by_id(id):
            flash("Cliente não encontrado.", "erro")
            return redirect(url_for("consulta_cliente"))

        clientes.update(id)
        flash("Cliente atualizado com sucesso.", "sucesso")
        return redirect(url_for("consulta_cliente"))
    except Exception as e:
        dados["id"] = id
        flash(f"Erro ao atualizar produto: {e}", "erro")
        return render_template("cad_cliente.html", produto=dados)
"""-----------FORNECEDORES-------------"""


def get_fornecedor_form():
    print("request",request.form) 
    return {
        "nome_fornecedor": request.form.get("nome_fornecedor", "").strip() .upper(),
        "cnpj_fornecedor": request.form.get("cnpj_fornecedor","").strip(),
        "email_fornecedor": request.form.get("email_fornecedor","").strip(),
        "tel_fornecedor": request.form.get("tel_fornecedor","").strip(),
        "cep_fornecedor": request.form.get("cep_fornecedor","").strip(),
        "ativado_fornecedor": to_int(request.form.get("ativado_fornecedor","")),
        "materia_prima_fornecedor":request.form.get("materia_prima_fornecedor", "").strip()
    }



'''Get fornecedores'''
@app.route("/fornecedor/<int:indice>", methods=["GET"])
def list_fornecedor(indice):
    if indice<=len(fornecedor):
        return jsonify(fornecedor[indice]),200
    return jsonify({"erro":"Fornecedor inexistente no sistema"}),404

'''Delete Fornecedores'''
@app.route("/fornecedor/<int:indice>", methods = ["DELETE"])
def del_fornecedore(indice):
    if indice < len(fornecedor):
        fornecedor.pop(indice)
        return jsonify({"mensagem": "Fornecedor removido com sucesso!"})
    return jsonify({"erro": "Fornecedor não encontrado"}), 404

'''Post Fornecedores'''
@app.route("/fornecedor", methods=["GET"])
def fornecedor():
    return render_template("cad_fornecedor.html")

@app.route("/cadastro/fornecedor", methods=["POST"])
def cad_fornecedor():
    dados = get_fornecedor_form()
    fornecedor = Fornecedor(**dados)
    try:
        fornecedor.insert()
        flash("Fornecedor cadastrado com sucesso.", "success")
        return redirect(url_for("fornecedor"))
    except Exception as e:
        flash(f"Erro ao cadastrar fornecedor: {e}", "danger")
    return render_template("cad_fornecedor.html")

'''Put Fornecedores'''
@app.route("/fornecedor/<int:indice>", methods=["PUT"])
def atualizar_forne(indice):
    if indice < len(fornecedor):
        att = request.get_json()
        ret = validar_put (att)
        if ret !=None:
            atualizar_fornecedor(indice, att, fornecedor)
            return jsonify({"mensagem": "Perfil atualizado com sucesso!"})
    return jsonify ({"erro": "Perfil não encontrado"}), 404

"""----------------MATERIA PRIMA--------------------"""

@app.route("/materiais", methods=["GET"])
def materiais():
    return render_template("cad_materiais.html")

@app.route("/materia-prima", methods=["GET"])
def materia_prima():
    return render_template("cad_materiais.html")


def get_materiais_form():
    print("request",request.form) 
    return {
        "nome_fornecedor": request.form.get("nome_fornecedor", "").strip() .upper(),
        "cnpj_fornecedor": request.form.get("cnpj_fornecedor","").strip(),
        "email_fornecedor": request.form.get("email_fornecedor","").strip(),
        "tel_fornecedor": request.form.get("tel_fornecedor","").strip(),
        "cep_fornecedor": request.form.get("cep_fornecedor","").strip(),
        "ativado_fornecedor": to_int(request.form.get("ativado_fornecedor","")),
        "materia_prima_fornecedor":request.form.get("materia_prima_fornecedor", "").strip()
    }

'''Get Materiais'''
@app.route("/materiais/<int:indice>", methods=["GET"])
def list_material(indice):
    if indice<=len(materiais):
        return jsonify(materiais[indice]),200
    return jsonify({"erro":"Material inexistente no sistema"}),404

'''Delete Materiais'''
@app.route("/materiais/<int:indice>", methods = ["DELETE"])
def deletar_materiais(indice):
    if indice < len(materiais):
        materiais.pop(indice)
        return jsonify({"mensagem": "material removido com sucesso!"})
    return jsonify({"erro": "material não encontrado"}), 404

'''Post Materiais'''
@app.route("/materiais", methods=["POST"])
def material_incluir():
    dados = request.form.to_dict()
    mp = Materia_prima(**dados)
    try:
        mp.insert()
        flash("Material cadastrado com sucesso.", "success")
        return redirect(url_for("materiais"))
    except Exception as e:
        flash(f"Erro ao cadastrar: {e}", "danger")
    return render_template("cad_materiais.html")

'''Put Materiais'''
@app.route("/materiais/<int:indice>", methods=["PUT"])
def atualizar_materi(indice):
    att = request.get_json()
    ret = validar_put (att)
    if ret !=None:
        atualizar_materiais(indice, att, materiais)
        return jsonify({"mensagem": "Material atualizado com sucesso!"})
    return jsonify ({"erro": "Material não encontrado"}), 404

"""----------------PEDIDO CLIENTE--------------------"""


def get_ped_cliente_form():
    print("request",request.form) 
    return {
        "d_realizacao_pedido_cliente": request.form.get("d_realizacao_pedido_cliente", "").strip() .upper(),
        "quantidade_pedido_cliente": request.form.get("quantidade_pedido_cliente","").strip(),
        "valor_unt_pedido_cliente": request.form.get("valor_unt_pedido_cliente","").strip(),
        "valor_total_pedido_cliente": request.form.get("valor_total_pedido_cliente","").strip(),
        "prazo_final_pedido_cliente": request.form.get("prazo_final_pedido_cliente","").strip(),
        "op_pedido_cliente":  request.form.get("op_pedido_cliente","").strip(),
    }

'''Get PEDIDO CLIENTE'''

@app.route("/pedido_cliente",methods=["GET"])
def pedido_clientes():
    return render_template ("pedido_cliente.html")

'''Delete PEDIDO CLIENTE'''
@app.route("/pedido_cliente/<int:indice>", methods=["DELETE"])
def deletar_ped_cliente(indice):
    if indice < len(ped_clientes):
        ped_clientes.pop(indice)
        return jsonify({"mensagem": "pedido de cliente removido com sucesso!"})
    return jsonify({"erro":"pedido de cliente não encontrado"}), 404

'''Post PEDIDO CLIENTE'''
@app.route("/pedido_cliente", methods=["POST"])
def pedido_ped_cliente():
    dados = get_ped_cliente_form()
    try:
        ped_cli = PedidoCliente(**dados)
        ped_cli.insert()
        flash("Pedido cadastrado com sucesso.", "success")
        return redirect(url_for("pedido_clientes"))
    except Exception as e:
        flash(f"Erro ao cadastrar pedido: {e}", "danger")
    return render_template("pedido_cliente.html")

'''Put PEDIDO CLIENTE'''
@app.route("/pedido_cliente/<int:indice>", methods=["PUT"])
def atualizar_ped_cliente(indice):
    info = request.get_json()
    if validar_put(info) !=None:
        atualizar_pedidocliente(indice, info, ped_clientes)
        return jsonify({"mensagem": "Pedido atualizado com sucesso!"})
    return jsonify ({"erro": "Pedido não encontrado"}), 404         
'''Mensagem PEDIDO NÃO ENCONTRADO'''

"""----------------PRODUÇÃO--------------------"""
@app.route("/producao", methods=["GET"])
def producao():
    return render_template("producao.html")


def get_producao_form():
    print("request",request.form) 
    return {
        "etapa_producao": request.form.get("etapa_producao", "").strip() .upper(),
        "status_producao": request.form.get("status_producao","").strip(),
        "valor_unt_pedido_cliente": request.form.get("valor_unt_pedido_cliente","").strip(),
        "valor_total_pedido_cliente": request.form.get("valor_total_pedido_cliente","").strip(),
        "prazo_final_pedido_cliente": request.form.get("prazo_final_pedido_cliente","").strip(),
        "op_pedido_cliente":  request.form.get("op_pedido_cliente","").strip(),
    }

'''Get PRODUÇÃO'''
@app.route("/producao/<int:indice>", methods=["GET"])
def buscar_producao(indice):
    if 0 <= indice < len(producao):
        return jsonify(producao[indice])
    return jsonify({"erro":"Produto não encontrado"})

'''Delete PRODUÇÃO'''
@app.route("/producao/<int:indice>", methods=["DELETE"])
def deletar_producao(indice):
    if indice < len(producao):
        producao.pop(indice)
        return jsonify({"mensagem": "item de producao removido"})
    return jsonify({"erro":"item de producao não encontrado"}), 404

'''Post PRODUÇÃO'''
@app.route("/producao", methods=["POST"])
def producao_incluir():
    dados=request.get_json()
    ret=validar_post(dados)
    if ret:
        return({"valido":True, "mensagem": "cadastro valido"})
    return({"valido": False, "mensagem": "cadastro invalido"})

'''Put PRODUÇÃO'''
@app.route("/producao/<int:indice>", methods=["PUT"])
def atualizar_prod(indice):
    if indice < len(processo):
        att = request.get_json()
        ret = validar_put (att)
        if ret !=None:
           atualizar_producao(indice, att, processo)
        return jsonify({"mensagem": "Produção atualizada com sucesso!"})
    return jsonify ({"erro": "Produção não encontrada"}), 404

"""----------------PEDIDO FORNECEDOR--------------------"""

def get_ped_fornecedor_form():
    print("request",request.form) 
    return {
        "d_entrega_pedido_fornecedor": request.form.get("d_entrega_pedido_fornecedor", "").strip() .upper(),
        "d_realizado_pedido_fornecedor": request.form.get("d_realizado_pedido_fornecedor","").strip(),
        "quantidade_pedido_fornecedor": request.form.get("quantidade_pedido_fornecedor","").strip(),
        "item_pedido_pedido_fornecedor": request.form.get("item_pedido_pedido_fornecedor","").strip()
    }

'''Get PEDIDO FORNECEDOR'''

@app.route("/pedido_fornecedor" , methods=["GET"])
def pedido_fornecedor():
    return render_template("pedido_fornecedor.html")

'''Delete PEDIDO FORNECEDOR'''
@app.route("/pedido_fornecedor/<int:indice>", methods = ["DELETE"])
def del_ped_fornecedores(indice):
    if indice < len(ped_fornecedor):
        ped_fornecedor.pop(indice)
        return flash("Pedido deletado")

'''Post PEDIDO FORNECEDOR'''
@app.route("/p_fornecedor", methods=["POST"])
def cad_ped_fornecedor():
    dados = get_ped_fornecedor_form()
    try:
        ped_forn = PedidoFornecedor(**dados)
        ped_forn.insert()
        flash("Pedido cadastrado com sucesso.", "success")
        return redirect(url_for("pedido_fornecedor"))
    except Exception as e:
        flash(f"Erro ao cadastrar pedido: {e}", "danger")
    return render_template("pedido_fornecedor.html")

'''Put PEDIDO FORNECEDOR'''
@app.route("/pedido_fornecedor/<int:indice>", methods=["PUT"])
def atualizar_ped_fornecedor(indice):
    dados = request.get_json()
    if validar_put(dados) !=None:
        atualizar_pedido_fornecedor(indice, dados, ped_fornecedor)
        return jsonify({"mensagem": "Livro atualizado com sucesso!"})
    return jsonify ({"erro": "Livro não encontrado"}), 404

print(pedido_fornecedor)

"""----------------FUNCIONÁRIOS--------------------"""


def get_funcionario_form():
    return {
        "nome_funcionario": request.form.get("nome_funcionario", "").strip().upper(),
        "tel_funcionario": request.form.get("tel_funcionario","").strip(),
        "email_funcionario": request.form.get("email_funcionario","").strip(),
        "cpf_funcionario": request.form.get("cpf_funcionario","").strip(),
        "classificacao_funcionario": request.form.get("classificacao_funcionario","").strip(),
        "cep_funcionario": request.form.get("cep_funcionario","").strip(),
        "foto_nome": request.form.get("foto_nome","").strip(),
        "foto_localizacao": request.form.get("foto_localizacao","").strip(),
        "foto_blob": request.form.get("foto_blob","").strip(),
        "num_clt_funcionario": request.form.get("num_clt_funcionario","").strip(),
        "senha_funcionario": request.form.get("senha_funcionario","").strip(),
        "ativado_funcionario": to_int(request.form.get("ativado_funcionario",""))
    }
#>>>>>>>>>>pra renderizar a tela<<<<<<<<<<<
@app.route("/funcionario" , methods=["GET"])
def funcionario():
    return render_template("cad_funcionario.html", )

'''Get Funcionários'''
@app.route("/funcionario/<int:indice>", methods=["GET"])
def buscar_funcionario(indice):
    if indice<=len(funcionarios):
        return jsonify(funcionarios[indice])
    return jsonify({"erro":"Funcionario não encontrado"}), 404

'''Delete Funcionários'''
@app.route("/funcionario/<int:indice>", methods = ["DELETE"])
def deletar_funcionarios(indice):
    if indice < len(funcionarios):
        funcionarios.pop(indice)
        return jsonify({"mensagem": "funcionario removido com sucesso!"})
    return jsonify({"erro": "funcionario não encontrado"}), 404

'''Post Funcionários'''
@app.route("/funcionario", methods=["POST"])
def funcionario_incluir():
    dados = get_funcionario_form()
    senha_texto = dados.get("senha_funcionario")
    dados["senha_funcionario"] = gerar_hash_senha(senha_texto)
    funcionario = Funcionario(**dados)
    try:
        funcionario.insert(dados)
        flash("Novo funcionário cadastrado com sucesso.", "success")
        return redirect(url_for("funcionario"))
    except Exception as e:
        flash(f"Erro ao cadastrar : {e}", "danger")
    return render_template("cad_funcionario.html")


'''Put Funcionários'''
@app.route("/funcionario/<int:indice>", methods=["PUT"])
def atualizar_func(indice):
    if indice < len(funcionarios):
        att = request.get_json()
        ret = validar_put(att)
        if ret !=None:
           atualizar_funcionarios(indice, att,funcionarios)
        return jsonify({"mensagem": "Material atualizado com sucesso!"})
    return jsonify ({"erro": "Material  não encontrado"}), 404

"""------------------ITEM-PEDIDO-----------------"""

'''Get Item-Pedido'''
@app.route("/itempedido", methods=["GET"])
def ites_pedido_get():
    item = request.get_json() if request.is_json else {}
    return jsonify(item)

@app.route("/itempedido/<int:indice>", methods=["GET"])
def itens_pedido(indice):
    if indice<=len(item_pedido):
        return jsonify(item_pedido[indice])
    return jsonify({"erro":"Item não encontrado."}),404

'''Delete Item-Pedido'''
@app.route("/itempedido/<int:indice>", methods = ["DELETE"])
def deletar_item_pedido(indice):
    if indice < len(item_pedido):
        item_pedido.pop(indice)
        return jsonify({"mensagem": "item pedido removido com sucesso!"})
    return jsonify({"erro": "item pedido não encontrado"}), 404

'''Post Item-Pedido'''
@app.route("/itempedido", methods=["POST"])
def Item_incluir():
    dados = request.get_json()
    retorno = validar_post(dados)
    if retorno == True:
        return {"valido": True, "mensagem": "Item adcionado ao pedido!"}
    else:
        return {"valido": False, "mensagem": "Algo deu errado..."}

'''Put Item-Pedido'''
@app.route("/item_pedido/<int:indice>", methods=["PUT"])
def atualizar_tabela_itempedido(indice):
    if indice <= len(item_pedido):
        info = request.get_json()
        if validar_put (info) !=None:
            atualizar_item_pedido(indice, info, item_pedido)
            return jsonify({"mensagem": "Item atualizado no pedido!"})
    return jsonify ({"erro": "Item não encontrado"}), 404

"""----------O QUE VAI (Ficha Técnica)-------------"""

"""Get Oque Vai"""
@app.route("/oque_vai", methods=["GET"])
def oque_vai():
    data = request.get_json() if request.is_json else {}
    return jsonify(data)

@app.route("/oqvai/<int:indice>", methods=["GET"])
def o_q_vai(indice):
    if indice<=len(oque_vai):
        return jsonify(oque_vai[indice])
    return jsonify({"erro":"Material não encontrado."}),404

"""Delete Oque Vai"""
@app.route("/oque_vai/<int:indice>", methods = ["DELETE"])
def deletar_oque_vai(indice):
    if indice < len(oque_vai):
        oque_vai.pop(indice)
        return jsonify({"mensagem": "ficha técnica removida com sucesso!"})
    return jsonify({"erro": "ficha técnica não encontrada"}), 404

"""Post Oque Vai"""
@app.route("/oque_vai", methods=["POST"])
def oque_vai_incluir():
    dados = request.get_json()
    retorno = validar_post(dados)
    if retorno == True:
        return {"valido": True, "mensagem": "ficha técnica criada!"}
    else:
        return {"valido": False, "mensagem": "Algo deu errado..."}

"""Put Oque Vai"""
@app.route("/oque_vai/<int:indice>", methods=["PUT"])
def atualizar_tabela_oquevai(indice):
    if indice <= len(oque_vai):
        info = request.get_json()
        if validar_put (info) !=None:
            atualizar_oque_vai(indice, info, oque_vai)
            return jsonify({"mensagem": "lista de materiais atualizada com sucesso!"})
    return jsonify ({"erro": "Lista não encontrada"}), 404

"""------------------PAGAMENTO--------------------"""

'''Get Pagamento'''
@app.route("/pagamento/<int:indice>", methods=["GET"])
def buscar_pagamento(indice):
    if indice<=len(pagamento):
        return jsonify(pagamento[indice])
    return jsonify({"erro":"Pagamento não sucedido"}),404

'''Delete Pagamento'''
@app.route("/pagamento/<int:indice>", methods = ["DELETE"])
def deletar_pagamentos(indice):
    if indice < len(pagamento):
        pagamento.pop(indice)
        return jsonify({"mensagem": "pagamento removido com sucesso!"})
    return jsonify({"erro": "pagamento não encontrado"}), 404

'''Post Pagamento'''
@app.route("/pagamento", methods=["POST"])
def pagamento_incluir():
    dados = request.get_json()
    retorno = validar_post(dados)
    if retorno  == True:
        return {"valido": True, "mensagem": "Pagamento ok!"}
    else:
        return{"valido":False, "mensagem": "Pagamento inválido!"}
'''Put Pagamento'''
@app.route("/pagamento/<int:indice>", methods=["PUT"])
def atualizar_pag(indice):
    if indice < len(pagamento):
        att = request.get_json()
        ret = validar_put (att)
        if ret !=None:
           atualizar_pagamentos(indice, att,pagamento)
        return jsonify({"mensagem": "Material atualizado com sucesso!"})
    return jsonify ({"erro": "Material  não encontrado"}), 404

"""--------------ESTOQUE FINAL------------------"""

'''Get Estoque Final'''
@app.route("/estoque/final" , methods=["GET"])
def final_estoque():
    return jsonify(estoquefinal)

'''Delete Estoque Final'''
@app.route("/estoque/final/<int:indice>", methods = ["DELETE"])
def deletar_estoque_final(indice):
    if indice < len(estoquefinal):
        estoquefinal.pop(indice)
        return jsonify({"mensagem": "item removido do estoque final com sucesso!"})
    return jsonify({"erro": "item não encontrado no estoque final"}), 404

'''Post Estoque Final'''
@app.route("/estoque/final", methods=["POST"])
def estoque_final():
    dados = request.get_json()
    retorno = validar_post(dados)
    if retorno == True:
        return {"valido": True, "mensagem": "Estoque final ok!"}
    else:
        return {"valido": False, "mensagem": " Estoque final inválido!"}

'''Put Estoque Final'''
@app.route("/estoque/final/<int:indice>", methods=["PUT"])
def atualizar_estqfim(indice):
    att = request.get_json()
    ret = validar_put (att)
    if ret !=None:
        atualizar_itens(indice, att, itens)
        return jsonify({"mensagem": "Estoque atualizado com sucesso!"})
    return jsonify ({"erro": "Estoque não encontrado"}), 404

'''============Validação============'''
def validar_post(dados):
    if len(dados) >= 1:
        return True
    return False

def validar_put(dados):
    print("clonagem dados recebidos: ", len(dados))#só pra conferir
    if len(dados) >= 1 :
        return {"mensagem": "feito"}
    return None

'''>>>>>>>>>>>>>>>>>>>>>>historico de compra-inicio<<<<<<<<<<<<<<<<<<<'''
hist=[]

#get
@app.route("/histcompra" , methods=["GET"])
def hist_compra():
    compra= request.get_json() if request.is_json else {}
    return jsonify (compra)

#get-parametro
@app.route("/histcompra/<int:indice>", methods=["GET"])
def compras(indice):
    if indice<=len(hist):
        return jsonify(hist[indice])
    return jsonify({"erro":"Pagamento não sucedido"}),404

#post
@app.route("/histcompra", methods=["POST"])
def hitorico_comprar():
    dados = request.get_json()
    if dados: 
        return{"Adicionado ao histórico": dados}

#put
@app.route("/histcompra/<int:indice>", methods=["PUT"])
def att_hist(indice):
    att = request.get_json()
    ret = validar_put (att)
    if ret !=None:
        atualizar_itens(indice, att, itens)
        return jsonify({"mensagem": "Histórico atualizado!"}), 201
    return jsonify ({"erro": "Histórico de compras não encontrado"}), 404

#delete
@app.route("/histcompra/<int:indice>", methods = ["DELETE"])
def del_compra(indice):
    if indice < len(hist):
        hist.pop(indice)
        return jsonify({"mensagem": "Histórico de compra excluído com sucesso!"}), 201
    return jsonify({"erro": "Histórico não encontrado"}), 404

'''>>>>>>>>>>>>>>>>>>>>>>historico de compra-fim<<<<<<<<<<<<<<<<<<<'''

'''>>>>>>>>>>>>>>histórico de venda-inicio<<<<<<<<<<<<<<<'''


#get 
@app.route("/histvenda" , methods=["GET"])
def hist_venda():
    ven= request.get_json() if request.is_json else {}
    return jsonify (ven)

#get-parametro
@app.route("/histvenda/<int:indice>", methods=["GET"])
def ver_venda(indice):
    if indice<=len(venda):
        return jsonify(venda[indice])
    return jsonify({"erro":"Histórico de compra não encontrdo"}),404

#post
@app.route("/histvenda", methods=["POST"])
def ins_venda():
    dados = request.get_json()
    if dados: 
        return{"Adicionado ao histórico": dados}

#put
@app.route("/histvenda/<int:indice>", methods=["PUT"])
def att_venda(indice):
    att = request.get_json()
    ret = validar_put (att)
    if ret !=None:
        atualizar_itens(indice, att, itens)
        return jsonify({"mensagem": "Histórico atualizado!"}), 201
    return jsonify ({"erro": "Histórico de venda não encontrado"}), 404

#delete
@app.route("/histvenda/<int:indice>", methods = ["DELETE"])
def del_venda(indice):
    if indice < len(venda):
        venda.pop(indice)
        return jsonify({"mensagem": "Histórico de venda excluído com sucesso!"}), 201
    return jsonify({"erro": "Histórico não encontrado"}), 404



'''============================  ENTRADA MATERIAL ==========================================='''

#get parametro
@app.route("/entrada/<int:indice>", methods=["GET"])
def ver_entrada(indice):
    if indice<=len(ef):
        return jsonify(ef[indice])
    return jsonify({"erro":"Entrada do pedido não encontrdo"}),404

#post
@app.route("/entrada", methods=["POST"])
def ins_entrada():
    dados = request.get_json()
    if dados: 
        return{"Adicionado as entradas de pedido": dados}

#put
@app.route("/entrada/<int:indice>", methods=["PUT"])
def att_entrada(indice):
    att = request.get_json()
    ret = validar_put (att)
    if ret !=None:
        atualizar_itens(indice, att, itens)
        return jsonify({"mensagem": "Entrada atualizado!"}), 201
    return jsonify ({"erro": "Registro de entrada não encontrado"}), 404

#delete
@app.route("/entrada/<int:indice>", methods = ["DELETE"])
def del_entrada_forn(indice):
    if indice < len(ef):
        ef.pop(indice)
        return jsonify({"mensagem": "Registro de entrada excluído com sucesso!"}), 201
    return jsonify({"erro": " Registro de entrada não encontrado"}), 404



'''========================== ENVIOS ===================================='''

#GET ENVIOS 

@app.route("/envios", methods=["GET"])
def rend_envio():
    return render_template("envios.html")


'''============================ ENVIOS DO DIA========================================'''
@app.route("/envio/envioDiario", methods= ["GET"])
def rend_envd():
   return render_template("envios_do_dia.html")


'''============================== MOVIMENTAÇÕES  ====================================='''

@app.route("/movimentacao", methods = ["GET"])
def rend_movimentacao():
        return render_template("movimentacoes.html")


'''============================= LOGOUT ========================================'''


@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu do sistema.", "info")
    return redirect(url_for("login"))


'''===================REDEFINIR SENHA==================='''
@app.route("/senha")
def nova_senha():
        return render_template ("redef.html")

if __name__=="__main__":
    app.run(debug=True)