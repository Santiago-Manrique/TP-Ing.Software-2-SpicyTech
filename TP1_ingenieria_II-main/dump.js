const fs = require('fs');
const path = require('path');

// 1. Adaptado para Spicy Coworking (Python, Web, Markdown)
const allowedExtensions = ['.py', '.js', '.html', '.css', '.md'];

// 2. Carpetas prohibidas (¡Para que no colapse la IA!)
const ignoreDirs = ['node_modules', '.git', '__pycache__', 'venv', 'env'];

function generateTree(dir, prefix = '') {
  if (!fs.existsSync(dir)) return '';
  const entries = fs.readdirSync(dir);
  let tree = '';

  entries.forEach((entry, index) => {
    const fullPath = path.join(dir, entry);
    
    // Ignorar carpetas pesadas
    if (ignoreDirs.includes(entry)) return;

    const isLast = index === entries.length - 1;
    const connector = isLast ? '┗' : '┣';
    const subPrefix = prefix + (isLast ? '  ' : '┃ ');

    tree += `${prefix}${connector} ${entry}\n`;

    if (fs.statSync(fullPath).isDirectory()) {
      tree += generateTree(fullPath, subPrefix);
    }
  });
  return tree;
}

function walk(dir, fileList = []) {
  if (!fs.existsSync(dir)) return fileList;

  fs.readdirSync(dir).forEach(file => {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);

    if (stat.isDirectory()) {
      if (!ignoreDirs.includes(file)) {
        walk(fullPath, fileList);
      }
    } else {
      const ext = path.extname(fullPath);
      if (allowedExtensions.includes(ext)) {
        const content = fs.readFileSync(fullPath, 'utf8');
        // Ajuste estético para Python en Markdown
        const lang = ext === '.py' ? 'python' : ext.slice(1);
        fileList.push(`## ${fullPath}\n\n\`\`\`${lang}\n${content}\n\`\`\`\n`);
      }
    }
  });
  return fileList;
}

// Escanea todo el proyecto desde la raíz
const targetPath = path.join(__dirname, '.');
const tree = generateTree(targetPath);
const files = walk(targetPath);

const markdown = `# Estructura del Proyecto\n\n\`\`\`\n${tree}\`\`\`\n\n# Contenido de Archivos\n\n${files.join('\n')}`;

// Guarda el archivo
fs.writeFileSync(path.join(__dirname, 'project_dump.md'), markdown);
console.log('Contexto generado con éxito: project_dump.md');
