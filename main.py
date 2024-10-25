from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QTextBrowser, QTabWidget, QInputDialog
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

DATABASE_URL = "mysql+pymysql://root:@localhost/gibis"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Gibi(Base):
    __tablename__ = 'gibis'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    titulo = Column(String, nullable=False)
    ano = Column(Integer, nullable=False)
    editora_id = Column(Integer, ForeignKey('editoras.id'), nullable=False)
    autor_id = Column(Integer, ForeignKey('autores.id'), nullable=False)
    categoria_id = Column(Integer, ForeignKey('categorias.id'), nullable=False)
    editora = relationship("Editora", back_populates="gibis")
    autor = relationship("Autor", back_populates="gibis")
    categoria = relationship("Categoria", back_populates="gibis")

class Autor(Base):
    __tablename__ = 'autores'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    pais_origem = Column(String, nullable=False)
    gibis = relationship("Gibi", back_populates="autor")

class Editora(Base):
    __tablename__ = 'editoras'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cidade = Column(String, nullable=False)
    gibis = relationship("Gibi", back_populates="editora")

class Categoria(Base):
    __tablename__ = 'categorias'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    gibis = relationship("Gibi", back_populates="categoria")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def add_editora(nome, cidade):
    try:
        if not nome or not cidade:
            raise ValueError("Nome e cidade são obrigatórios.")
        editora = Editora(nome=nome, cidade=cidade)
        session.add(editora)
        session.commit()
        QMessageBox.information(None, "Sucesso", "Editora adicionada com sucesso.")
    except (SQLAlchemyError, ValueError) as e:
        session.rollback()
        QMessageBox.warning(None, "Erro", f"Erro ao adicionar editora: {e}")

def add_autor(nome, pais_origem):
    try:
        if not nome or not pais_origem:
            raise ValueError("Nome e país de origem são obrigatórios.")
        autor = Autor(nome=nome, pais_origem=pais_origem)
        session.add(autor)
        session.commit()
        QMessageBox.information(None, "Sucesso", "Autor adicionado com sucesso.")
    except (SQLAlchemyError, ValueError) as e:
        session.rollback()
        QMessageBox.warning(None, "Erro", f"Erro ao adicionar autor: {e}")

def add_categoria(nome):
    try:
        if not nome:
            raise ValueError("Nome da categoria é obrigatório.")
        categoria = Categoria(nome=nome)
        session.add(categoria)
        session.commit()
        QMessageBox.information(None, "Sucesso", "Categoria adicionada com sucesso.")
    except (SQLAlchemyError, ValueError) as e:
        session.rollback()
        QMessageBox.warning(None, "Erro", f"Erro ao adicionar categoria: {e}")

def add_gibi(titulo, ano, editora_id, autor_id, categoria_id):
    try:
        if not titulo or not ano or not editora_id or not autor_id or not categoria_id:
            raise ValueError("Todos os campos são obrigatórios.")
        gibi = Gibi(titulo=titulo, ano=ano, editora_id=editora_id, autor_id=autor_id, categoria_id=categoria_id)
        session.add(gibi)
        session.commit()
        QMessageBox.information(None, "Sucesso", "Gibi adicionado com sucesso.")
    except (SQLAlchemyError, ValueError) as e:
        session.rollback()
        QMessageBox.warning(None, "Erro", f"Erro ao adicionar gibi: {e}")

def update_gibi(gibi_id, novo_titulo, novo_ano, novo_editora_id, novo_autor_id, novo_categoria_id):
    try:
        gibi = session.query(Gibi).filter_by(id=gibi_id).first()
        if gibi:
            gibi.titulo = novo_titulo
            gibi.ano = novo_ano
            gibi.editora_id = novo_editora_id
            gibi.autor_id = novo_autor_id
            gibi.categoria_id = novo_categoria_id
            session.commit()
            QMessageBox.information(None, "Sucesso", "Gibi atualizado com sucesso.")
        else:
            raise ValueError("Gibi não encontrado.")
    except (SQLAlchemyError, ValueError) as e:
        session.rollback()
        QMessageBox.warning(None, "Erro", f"Erro ao atualizar gibi: {e}")

def delete_gibi(gibi_id):
    try:
        gibi = session.query(Gibi).filter_by(id=gibi_id).first()
        if gibi:
            session.delete(gibi)
            session.commit()
            QMessageBox.information(None, "Sucesso", "Gibi deletado com sucesso.")
        else:
            raise ValueError("Gibi não encontrado.")
    except (SQLAlchemyError, ValueError) as e:
        session.rollback()
        QMessageBox.warning(None, "Erro", f"Erro ao deletar gibi: {e}")

def update_autor(autor_id, novo_nome, novo_pais_origem):
    try:
        autor = session.query(Autor).filter_by(id=autor_id).first()
        if autor:
            autor.nome = novo_nome
            autor.pais_origem = novo_pais_origem
            session.commit()
            QMessageBox.information(None, "Sucesso", "Autor atualizado com sucesso.")
        else:
            raise ValueError("Autor não encontrado.")
    except (SQLAlchemyError, ValueError) as e:
        session.rollback()
        QMessageBox.warning(None, "Erro", f"Erro ao atualizar autor: {e}")

def delete_autor(autor_id):
    try:
        autor = session.query(Autor).filter_by(id=autor_id).first()
        if autor:
            session.delete(autor)
            session.commit()
            QMessageBox.information(None, "Sucesso", "Autor deletado com sucesso.")
        else:
            raise ValueError("Autor não encontrado.")
    except (SQLAlchemyError, ValueError) as e:
        session.rollback()
        QMessageBox.warning(None, "Erro", f"Erro ao deletar autor: {e}")

def update_editora(editora_id, novo_nome, nova_cidade):
    try:
        editora = session.query(Editora).filter_by(id=editora_id).first()
        if editora:
            editora.nome = novo_nome
            editora.cidade = nova_cidade
            session.commit()
            QMessageBox.information(None, "Sucesso", "Editora atualizada com sucesso.")
        else:
            raise ValueError("Editora não encontrada.")
    except (SQLAlchemyError, ValueError) as e:
        session.rollback()
        QMessageBox.warning(None, "Erro", f"Erro ao atualizar editora: {e}")

def delete_editora(editora_id):
    try:
        editora = session.query(Editora).filter_by(id=editora_id).first()
        if editora:
            session.delete(editora)
            session.commit()
            QMessageBox.information(None, "Sucesso", "Editora deletada com sucesso.")
        else:
            raise ValueError("Editora não encontrada.")
    except (SQLAlchemyError, ValueError) as e:
        session.rollback()
        QMessageBox.warning(None, "Erro", f"Erro ao deletar editora: {e}")

def update_categoria(categoria_id, novo_nome):
    try:
        categoria = session.query(Categoria).filter_by(id=categoria_id).first()
        if categoria:
            categoria.nome = novo_nome
            session.commit()
            QMessageBox.information(None, "Sucesso", "Categoria atualizada com sucesso.")
        else:
            raise ValueError("Categoria não encontrada.")
    except (SQLAlchemyError, ValueError) as e:
        session.rollback()
        QMessageBox.warning(None, "Erro", f"Erro ao atualizar categoria: {e}")

def delete_categoria(categoria_id):
    try:
        categoria = session.query(Categoria).filter_by(id=categoria_id).first()
        if categoria:
            session.delete(categoria)
            session.commit()
            QMessageBox.information(None, "Sucesso", "Categoria deletada com sucesso.")
        else:
            raise ValueError("Categoria não encontrada.")
    except (SQLAlchemyError, ValueError) as e:
        session.rollback()
        QMessageBox.warning(None, "Erro", f"Erro ao deletar categoria: {e}")

class GibiApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRUD Gibis")
        self.setGeometry(100, 100, 500, 800)
        layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.tab_gibis = QWidget()
        self.tab_autores = QWidget()
        self.tab_editoras = QWidget()
        self.tab_categorias = QWidget()
        self.setup_gibi_tab()
        self.setup_autor_tab()
        self.setup_editora_tab()
        self.setup_categoria_tab()
        self.tabs.addTab(self.tab_gibis, "Gibis")
        self.tabs.addTab(self.tab_autores, "Autores")
        self.tabs.addTab(self.tab_editoras, "Editoras")
        self.tabs.addTab(self.tab_categorias, "Categorias")
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def setup_gibi_tab(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        self.title_input = QLineEdit()
        self.year_input = QLineEdit()
        self.editora_input = QLineEdit()
        self.autor_input = QLineEdit()
        self.categoria_input = QLineEdit()
        form_layout.addRow(QLabel("Título:"), self.title_input)
        form_layout.addRow(QLabel("Ano:"), self.year_input)
        form_layout.addRow(QLabel("ID Editora:"), self.editora_input)
        form_layout.addRow(QLabel("ID Autor:"), self.autor_input)
        form_layout.addRow(QLabel("ID Categoria:"), self.categoria_input)
        layout.addLayout(form_layout)
        self.add_gibi_btn = QPushButton("Adicionar Gibi")
        self.add_gibi_btn.clicked.connect(self.add_gibi)
        self.list_gibi_btn = QPushButton("Listar Gibis")
        self.list_gibi_btn.clicked.connect(self.list_gibis)
        self.update_gibi_btn = QPushButton("Atualizar Gibi")
        self.update_gibi_btn.clicked.connect(self.show_update_gibi)
        self.delete_gibi_btn = QPushButton("Deletar Gibi")
        self.delete_gibi_btn.clicked.connect(self.show_delete_gibi)
        layout.addWidget(self.add_gibi_btn)
        layout.addWidget(self.list_gibi_btn)
        layout.addWidget(self.update_gibi_btn)
        layout.addWidget(self.delete_gibi_btn)
        self.tab_gibis.setLayout(layout)
        self.gibi_list = QTextBrowser()
        layout.addWidget(self.gibi_list)

    def setup_autor_tab(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        self.autor_nome_input = QLineEdit()
        self.autor_pais_input = QLineEdit()
        form_layout.addRow(QLabel("Nome:"), self.autor_nome_input)
        form_layout.addRow(QLabel("País de Origem:"), self.autor_pais_input)
        layout.addLayout(form_layout)
        self.add_autor_btn = QPushButton("Adicionar Autor")
        self.add_autor_btn.clicked.connect(self.add_autor)
        self.list_autor_btn = QPushButton("Listar Autores")
        self.list_autor_btn.clicked.connect(self.list_autores)
        self.update_autor_btn = QPushButton("Atualizar Autor")
        self.update_autor_btn.clicked.connect(self.show_update_autor)
        self.delete_autor_btn = QPushButton("Deletar Autor")
        self.delete_autor_btn.clicked.connect(self.show_delete_autor)
        layout.addWidget(self.add_autor_btn)
        layout.addWidget(self.list_autor_btn)
        layout.addWidget(self.update_autor_btn)
        layout.addWidget(self.delete_autor_btn)
        self.tab_autores.setLayout(layout)
        self.autor_list = QTextBrowser()
        layout.addWidget(self.autor_list)

    def setup_editora_tab(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        self.editora_nome_input = QLineEdit()
        self.editora_cidade_input = QLineEdit()
        form_layout.addRow(QLabel("Nome:"), self.editora_nome_input)
        form_layout.addRow(QLabel("Cidade:"), self.editora_cidade_input)
        layout.addLayout(form_layout)
        self.add_editora_btn = QPushButton("Adicionar Editora")
        self.add_editora_btn.clicked.connect(self.add_editora)
        self.list_editora_btn = QPushButton("Listar Editoras")
        self.list_editora_btn.clicked.connect(self.list_editoras)
        self.update_editora_btn = QPushButton("Atualizar Editora")
        self.update_editora_btn.clicked.connect(self.show_update_editora)
        self.delete_editora_btn = QPushButton("Deletar Editora")
        self.delete_editora_btn.clicked.connect(self.show_delete_editora)
        layout.addWidget(self.add_editora_btn)
        layout.addWidget(self.list_editora_btn)
        layout.addWidget(self.update_editora_btn)
        layout.addWidget(self.delete_editora_btn)
        self.tab_editoras.setLayout(layout)
        self.editora_list = QTextBrowser()
        layout.addWidget(self.editora_list)

    def setup_categoria_tab(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        self.categoria_nome_input = QLineEdit()
        form_layout.addRow(QLabel("Nome:"), self.categoria_nome_input)
        layout.addLayout(form_layout)
        self.add_categoria_btn = QPushButton("Adicionar Categoria")
        self.add_categoria_btn.clicked.connect(self.add_categoria)
        self.list_categoria_btn = QPushButton("Listar Categorias")
        self.list_categoria_btn.clicked.connect(self.list_categorias)
        self.update_categoria_btn = QPushButton("Atualizar Categoria")
        self.update_categoria_btn.clicked.connect(self.show_update_categoria)
        self.delete_categoria_btn = QPushButton("Deletar Categoria")
        self.delete_categoria_btn.clicked.connect(self.show_delete_categoria)
        layout.addWidget(self.add_categoria_btn)
        layout.addWidget(self.list_categoria_btn)
        layout.addWidget(self.update_categoria_btn)
        layout.addWidget(self.delete_categoria_btn)
        self.tab_categorias.setLayout(layout)
        self.categoria_list = QTextBrowser()
        layout.addWidget(self.categoria_list)

    def add_gibi(self):
        titulo = self.title_input.text()
        ano = self.year_input.text()
        editora_id = self.editora_input.text()
        autor_id = self.autor_input.text()
        categoria_id = self.categoria_input.text()
        add_gibi(titulo, ano, editora_id, autor_id, categoria_id)

    def list_gibis(self):
        gibis = session.query(Gibi).all()
        self.gibi_list.clear()
        for gibi in gibis:
            self.gibi_list.append(f"{gibi.id}: {gibi.titulo} ({gibi.ano})")

    def show_update_gibi(self):
        gibi_id, ok = QInputDialog.getText(self, "Atualizar Gibi", "Insira o ID do Gibi:")
        if ok:
            gibi = session.query(Gibi).filter_by(id=gibi_id).first()
            if gibi:
                self.title_input.setText(gibi.titulo)
                self.year_input.setText(str(gibi.ano))
                self.editora_input.setText(str(gibi.editora_id))
                self.autor_input.setText(str(gibi.autor_id))
                self.categoria_input.setText(str(gibi.categoria_id))
                self.update_gibi(gibi_id)
            else:
                QMessageBox.warning(self, "Erro", "Gibi não encontrado.")

    def update_gibi(self, gibi_id):
        novo_titulo = self.title_input.text()
        novo_ano = self.year_input.text()
        novo_editora_id = self.editora_input.text()
        novo_autor_id = self.autor_input.text()
        novo_categoria_id = self.categoria_input.text()
        update_gibi(gibi_id, novo_titulo, novo_ano, novo_editora_id, novo_autor_id, novo_categoria_id)

    def show_delete_gibi(self):
        gibi_id, ok = QInputDialog.getText(self, "Deletar Gibi", "Insira o ID do Gibi:")
        if ok:
            self.delete_gibi(gibi_id)

    def delete_gibi(self, gibi_id):
        delete_gibi(gibi_id)

    def add_autor(self):
        nome = self.autor_nome_input.text()
        pais_origem = self.autor_pais_input.text()
        add_autor(nome, pais_origem)

    def list_autores(self):
        autores = session.query(Autor).all()
        self.autor_list.clear()
        for autor in autores:
            self.autor_list.append(f"{autor.id}: {autor.nome} ({autor.pais_origem})")

    def show_update_autor(self):
        autor_id, ok = QInputDialog.getText(self, "Atualizar Autor", "Insira o ID do Autor:")
        if ok:
            autor = session.query(Autor).filter_by(id=autor_id).first()
            if autor:
                self.autor_nome_input.setText(autor.nome)
                self.autor_pais_input.setText(autor.pais_origem)
                self.update_autor(autor_id)
            else:
                QMessageBox.warning(self, "Erro", "Autor não encontrado.")

    def update_autor(self, autor_id):
        nome = self.autor_nome_input.text()
        pais_origem = self.autor_pais_input.text()
        update_autor(autor_id, nome, pais_origem)

    def show_delete_autor(self):
        autor_id, ok = QInputDialog.getText(self, "Deletar Autor", "Insira o ID do Autor:")
        if ok:
            self.delete_autor(autor_id)

    def delete_autor(self, autor_id):
        delete_autor(autor_id)

    def add_editora(self):
        nome = self.editora_nome_input.text()
        cidade = self.editora_cidade_input.text()
        add_editora(nome, cidade)

    def list_editoras(self):
        editoras = session.query(Editora).all()
        self.editora_list.clear()
        for editora in editoras:
            self.editora_list.append(f"{editora.id}: {editora.nome} ({editora.cidade})")

    def show_update_editora(self):
        editora_id, ok = QInputDialog.getText(self, "Atualizar Editora", "Insira o ID da Editora:")
        if ok:
            editora = session.query(Editora).filter_by(id=editora_id).first()
            if editora:
                self.editora_nome_input.setText(editora.nome)
                self.editora_cidade_input.setText(editora.cidade)
                self.update_editora(editora_id)
            else:
                QMessageBox.warning(self, "Erro", "Editora não encontrada.")

    def update_editora(self, editora_id):
        nome = self.editora_nome_input.text()
        cidade = self.editora_cidade_input.text()
        update_editora(editora_id, nome, cidade)

    def show_delete_editora(self):
        editora_id, ok = QInputDialog.getText(self, "Deletar Editora", "Insira o ID da Editora:")
        if ok:
            self.delete_editora(editora_id)

    def delete_editora(self, editora_id):
        delete_editora(editora_id)

    def add_categoria(self):
        nome = self.categoria_nome_input.text()
        add_categoria(nome)

    def list_categorias(self):
        categorias = session.query(Categoria).all()
        self.categoria_list.clear()
        for categoria in categorias:
            self.categoria_list.append(f"{categoria.id}: {categoria.nome}")

    def show_update_categoria(self):
        categoria_id, ok = QInputDialog.getText(self, "Atualizar Categoria", "Insira o ID da Categoria:")
        if ok:
            categoria = session.query(Categoria).filter_by(id=categoria_id).first()
            if categoria:
                self.categoria_nome_input.setText(categoria.nome)
                self.update_categoria(categoria_id)
            else:
                QMessageBox.warning(self, "Erro", "Categoria não encontrada.")

    def update_categoria(self, categoria_id):
        novo_nome = self.categoria_nome_input.text()
        update_categoria(categoria_id, novo_nome)

    def show_delete_categoria(self):
        categoria_id, ok = QInputDialog.getText(self, "Deletar Categoria", "Insira o ID da Categoria:")
        if ok:
            self.delete_categoria(categoria_id)

    def delete_categoria(self, categoria_id):
        delete_categoria(categoria_id)

if __name__ == "__main__":
    import sys  
    app = QApplication(sys.argv)
    window = GibiApp()
    window.show()
    sys.exit(app.exec_())
