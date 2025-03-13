const express = require('express');
const path = require('path');
const app = express();
const port = 3000;

// Configurar o diretório público para servir arquivos estáticos
app.use(express.static(path.join(__dirname, '..', 'public')));

// Rota para servir o arquivo HTML
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'public', 'chat_georgia.html'));
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
