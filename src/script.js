// Definindo as palavras proibidas (cursewords)
const bannedWords = ["curseword1", "curseword2", "curseword3"]; // Exemplo de palavras proibidas

// Função para submeter um comentário
function submitComment() {
    // Obter valores de entrada
    const user = document.getElementById("user").value.trim();
    const commentText = document.getElementById("comment_text").value.trim();
    const messageElement = document.getElementById("message");

    // Limpar a mensagem anterior
    messageElement.classList.add("hidden");
    messageElement.textContent = "";

    // Validar texto do comentário vazio
    if (commentText === "") {
        showMessage("Comment has no text", "error");
        return;
    }

    // Verificar se o comentário contém palavras proibidas
    if (containsBannedWords(commentText)) {
        showMessage("Comment contains inappropriate language", "error");
        return;
    }

    // Validar nome do usuário
    if (user === "") {
        showMessage("User name is required", "error");
        return;
    }

    // Criar um novo objeto de comentário
    const timestamp = new Date().toLocaleString();
    const comment = {
        user: user,
        text: commentText,
        timestamp: timestamp
    };

    // Armazenar o comentário no localStorage
    saveComment(comment);

    // Mostrar mensagem de sucesso
    showMessage(`Comment successfully submitted by ${user} on ${timestamp}.`, "success");

    // Limpar os campos do formulário após a submissão
    document.getElementById("user").value = "";
    document.getElementById("comment_text").value = "";

    // Exibir o novo comentário imediatamente
    addCommentToDisplay(comment);
}

// Função para verificar se o texto contém palavras proibidas
function containsBannedWords(text) {
    return bannedWords.some(word => text.toLowerCase().includes(word));
}

// Função auxiliar para exibir uma mensagem (erro ou sucesso)
function showMessage(message, type) {
    const messageElement = document.getElementById("message");
    messageElement.textContent = message;
    messageElement.classList.remove("hidden");
    messageElement.className = type === "error" ? "error" : "success";
}

// Salvar o comentário no localStorage
function saveComment(comment) {
    let comments = JSON.parse(localStorage.getItem("comments")) || [];
    comments.push(comment);
    localStorage.setItem("comments", JSON.stringify(comments));
}

// Carregar comentários do localStorage e exibi-los
function loadComments() {
    const comments = JSON.parse(localStorage.getItem("comments")) || [];
    comments.forEach(comment => addCommentToDisplay(comment));
}

// Adicionar um único comentário à seção de exibição
function addCommentToDisplay(comment) {
    const commentsContainer = document.getElementById("comments");

    const commentElement = document.createElement("div");
    commentElement.classList.add("comment");

    const userElement = document.createElement("p");
    userElement.textContent = `${comment.user}:`;
    commentElement.appendChild(userElement);

    const textElement = document.createElement("p");
    textElement.textContent = comment.text;
    commentElement.appendChild(textElement);

    const timestampElement = document.createElement("p");
    timestampElement.classList.add("timestamp");
    timestampElement.textContent = `Posted on: ${comment.timestamp}`;
    commentElement.appendChild(timestampElement);

    commentsContainer.appendChild(commentElement);
}

// Carregar os comentários ao carregar a página
window.onload = loadComments;
