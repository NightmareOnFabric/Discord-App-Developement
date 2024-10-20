Comandos Básicos de Git
git init

Descripción: Inicializa un nuevo repositorio Git en el directorio actual.
git clone [url]

Descripción: Crea una copia local de un repositorio remoto.
git add [archivo]

Descripción: Agrega un archivo específico al área de preparación (staging area) para el próximo commit.
git add .

Descripción: Agrega todos los archivos en el directorio actual al área de preparación.
git commit -m "[mensaje]"

Descripción: Registra los cambios en el repositorio con un mensaje de commit descriptivo.
git status

Descripción: Muestra el estado actual del repositorio, incluidos los archivos modificados, los que están en el área de preparación y los no rastreados.
git log

Descripción: Muestra el historial de commits en el repositorio.
git diff

Descripción: Muestra las diferencias entre el estado actual y el último commit.
Comandos de Ramas
git branch

Descripción: Lista todas las ramas en el repositorio actual.
git branch [nombre-rama]

Descripción: Crea una nueva rama con el nombre especificado.
git checkout [nombre-rama]

Descripción: Cambia a la rama especificada.
git checkout -b [nombre-rama]

Descripción: Crea y cambia a una nueva rama.
git merge [nombre-rama]

Descripción: Fusiona los cambios de la rama especificada a la rama actual.
git rebase [nombre-rama]

Descripción: Aplica los cambios de la rama actual sobre la rama especificada.
Comandos Remotos
git remote -v

Descripción: Muestra las URL de los repositorios remotos asociados.
git remote add [nombre] [url]

Descripción: Agrega un nuevo repositorio remoto con un nombre especificado.
git push [remoto] [rama]

Descripción: Envía los commits de la rama local al repositorio remoto.
git pull [remoto] [rama]

Descripción: Obtiene y fusiona cambios del repositorio remoto a la rama actual.
git fetch [remoto]

Descripción: Descarga los cambios del repositorio remoto, pero no los fusiona.
Comandos de Revisión y Deshacer
git reset [archivo]

Descripción: Deshace los cambios en un archivo del área de preparación.
git reset --hard

Descripción: Restablece el repositorio al último commit, descartando todos los cambios no confirmados.
git revert [commit]

Descripción: Crea un nuevo commit que deshace los cambios de un commit anterior.
git stash

Descripción: Guarda temporalmente los cambios no confirmados para limpiar el área de trabajo.
git stash pop

Descripción: Aplica los cambios guardados en el stash y los elimina del stash.
Comandos Avanzados
git cherry-pick [commit]

Descripción: Aplica un commit específico de otra rama a la rama actual.
git tag [nombre]

Descripción: Crea una etiqueta (tag) en el commit actual, a menudo usada para marcar versiones.
