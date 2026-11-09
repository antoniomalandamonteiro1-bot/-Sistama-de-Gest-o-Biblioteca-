from datetime import datetime, timedelta


class Pessoa:
    def __init__(self, id_pessoa: int, nome: str, email: str):
        self.__id = id_pessoa
        self.__nome = nome
        self.__email = email

    
    def get_id(self) -> int:
        return self.__id

    def get_nome(self) -> str:
        return self.__nome

    def get_email(self) -> str:
        return self.__email

    def autenticar(self) -> bool:
       
        print(f"Utilizador {self.__nome} autenticado com sucesso.")
        return True



class Leitor(Pessoa):
    def __init__(self, id_pessoa: int, nome: str, email: str, numero_leitor: str):
        super().__init__(id_pessoa, nome, email)
        self.__numero_leitor = numero_leitor
        self.__data_registo = datetime.now()

    def get_numero_leitor(self) -> str:
        return self.__numero_leitor

    def solicitar_emprestimo(self, exemplar, bibliotecario):
        print(f"\n[Solicitação] Leitor {self.get_nome()} solicitou o exemplar '{exemplar.get_livro().get_titulo()}' (Cód: {exemplar.get_codigo()}).")
        return bibliotecario.registar_emprestimo(self, exemplar)

    def reservar_livro(self, livro):
        print(f"[Reserva] Leitor {self.get_nome()} efectuou reserva para o livro '{livro.get_titulo()}'.")
        return Reserva(self, livro)



class Bibliotecario(Pessoa):
    def __init__(self, id_pessoa: int, nome: str, email: str, funcionario_id: str):
        super().__init__(id_pessoa, nome, email)
        self.__funcionario_id = funcionario_id

    def get_funcionario_id(self) -> str:
        return self.__funcionario_id

    def registar_emprestimo(self, leitor: Leitor, exemplar):
        if exemplar.get_estado() == "Disponível":
            exemplar.set_estado("Emprestado")
            emprestimo = Emprestimo(leitor, self, exemplar)
            print(f"[Sucesso] Empréstimo registado pelo bibliotecário {self.get_nome()}.")
            return emprestimo
        else:
            print(f"[Erro] O exemplar {exemplar.get_codigo()} não está disponível (Estado: {exemplar.get_estado()}).")
            return None

    def registar_devolucao(self, emprestimo):
        emprestimo.finalizar()
        print(f"[Devolução] Bibliotecário {self.get_nome()} registou a devolução do exemplar.")



class Livro:
    def __init__(self, isbn: str, titulo: str, autor: str, categoria: str):
        self.__isbn = isbn
        self.__titulo = titulo
        self.__autor = autor
        self.__categoria = categoria
        self.__exemplares = []  

    def get_isbn(self) -> str:
        return self.__isbn

    def get_titulo(self) -> str:
        return self.__titulo

    def adicionar_exemplar(self, exemplar):
        self.__exemplares.append(exemplar)

    def consultar_disponibilidade(self) -> bool:
        for ex in self.__exemplares:
            if ex.get_estado() == "Disponível":
                return True
        return False



class Exemplar:
    def __init__(self, codigo: str, localizacao: str, livro: Livro):
        self.__codigo = codigo
        self.__estado = "Disponível"  
        self.__localizacao = localizacao
        self.__livro = livro
        livro.adicionar_exemplar(self) 

    def get_codigo(self) -> str:
        return self.__codigo

    def get_estado(self) -> str:
        return self.__estado

    def set_estado(self, estado: str):
        self.__estado = estado

    def get_livro(self) -> Livro:
        return self.__livro

    def marcar_disponivel(self):
        self.__estado = "Disponível"



class Emprestimo:
    _contador_id = 1

    def __init__(self, leitor: Leitor, bibliotecario: Bibliotecario, exemplar: Exemplar):
        self.__id = Emprestimo._contador_id
        Emprestimo._contador_id += 1
        self.__data_emprestimo = datetime.now()
        self.__data_prevista = self.__data_emprestimo + timedelta(days=14)  # 2 semanas de prazo
        self.__data_devolucao = None
        self.__leitor = leitor
        self.__bibliotecario = bibliotecario
        self.__exemplar = exemplar

    def calcular_atraso(self) -> int:
        hoje = datetime.now()
        if not self.__data_devolucao and hoje > self.__data_prevista:
            atraso = (hoje - self.__data_prevista).days
            return atraso
        return 0

    def finalizar(self):
        self.__data_devolucao = datetime.now()
        self.__exemplar.marcar_disponivel()



class Reserva:
    _contador_id = 1

    def __init__(self, leitor: Leitor, livro: Livro):
        self.__id = Reserva._contador_id
        Reserva._contador_id += 1
        self.__data_reserva = datetime.now()
        self.__estado = "Pendente"
        self.__leitor = leitor
        self.__livro = livro

    def cancelar(self):
        self.__estado = "Cancelado"
        print(f"Reserva {self.__id} cancelada.")

    def confirmar(self):
        self.__estado = "Confirmado"
        print(f"Reserva {self.__id} confirmada.")



if __name__ == "__main__":
    print("--- SISTEMA DE GESTÃO DE BIBLIOTECA (DEMONSTRAÇÃO) ---")

    livro1 = Livro("978-989-123-456-7", "Engenharia de Software", "Ian Sommerville", "Tecnologia")
    exemplar1 = Exemplar("EX-001", "Estante A1", livro1)
    exemplar2 = Exemplar("EX-002", "Estante A1", livro1)


    leitor1 = Leitor(1, "Ana Silva", "ana@email.com", "L-2026-001")
    bibliotecario1 = Bibliotecario(2, "Carlos Mello", "carlos@biblioteca.com", "B-998")

 
    leitor1.autenticar()
    bibliotecario1.autenticar()


    print(f"\nO livro '{livro1.get_titulo()}' está disponível? {'Sim' if livro1.consultar_disponibilidade() else 'Não'}")

    
    emprestimo1 = leitor1.solicitar_emprestimo(exemplar1, bibliotecario1)

    
    print("\nTentativa de re-emprestar o mesmo exemplar:")
    leitor1.solicitar_emprestimo(exemplar1, bibliotecario1)

    
    if emprestimo1:
        print("\nProcesso de devolução:")
        bibliotecario1.registar_devolucao(emprestimo1)
        print(f"O livro '{livro1.get_titulo()}' está disponível novamente? {'Sim' if livro1.consultar_disponibilidade() else 'Não'}")
