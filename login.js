async function fazerLogin() {
    const email = document.getElementById("emailCliente").value;
    const senha = document.getElementById("senhaCliente").value;

    try {
        // Certifique-se de que a porta seja a mesma onde o Flask roda (ex: 5000)
        const response = await fetch("http://localhost:5000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email_funcionario: email,
                senha_funcionario: senha
            })
        });

        const dados = await response.json();

        if (response.ok) {
            alert(dados.mensagem);
            // Redireciona via JS após o login bem-sucedido
            window.location.href = "home.html";
        } else {
            alert(dados.mensagem || "E-mail ou senha inválidos.");
        }
    } catch (error) {
        console.error("Erro ao conectar com o servidor:", error);
        alert("Não foi possível conectar ao servidor. Verifique se o Flask está rodando!");
    }
}