from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List


class Perfil(str, Enum):
    USUARIO = "usuario"
    TECNICO = "tecnico"
    ADMINISTRADOR = "administrador"


class Prioridade(str, Enum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"


class Status(str, Enum):
    ABERTO = "aberto"
    EM_ATENDIMENTO = "em_atendimento"
    RESOLVIDO = "resolvido"
    CANCELADO = "cancelado"


@dataclass(slots=True)
class Usuario:
    id: int
    nome: str
    email: str
    perfil: Perfil
    ativo: bool = True


@dataclass(slots=True)
class Historico:
    mensagem: str
    autor: Usuario
    criado_em: datetime = field(default_factory=datetime.now)


@dataclass(slots=True)
class Chamado:
    id: int
    titulo: str
    descricao: str
    laboratorio: str
    prioridade: Prioridade
    autor: Usuario
    status: Status = Status.ABERTO
    historico: List[Historico] = field(default_factory=list)
    criado_em: datetime = field(default_factory=datetime.now)
    atualizado_em: datetime = field(default_factory=datetime.now)

    def adicionar_historico(self, mensagem: str, autor: Usuario) -> None:
        self.historico.append(Historico(mensagem=mensagem, autor=autor))
        self.atualizado_em = datetime.now()

    def alterar_status(self, novo_status: Status, usuario: Usuario) -> None:
        if usuario.perfil not in {Perfil.TECNICO, Perfil.ADMINISTRADOR}:
            raise PermissionError("Somente técnico ou administrador pode alterar status.")

        status_anterior = self.status
        self.status = novo_status
        self.adicionar_historico(
            mensagem=f"Status alterado de {status_anterior.value} para {novo_status.value}.",
            autor=usuario,
        )


class SistemaChamados:
    def __init__(self) -> None:
        self._chamados: list[Chamado] = []
        self._proximo_id = 1

    def abrir_chamado(
        self,
        titulo: str,
        descricao: str,
        laboratorio: str,
        prioridade: Prioridade,
        autor: Usuario,
    ) -> Chamado:
        if not autor.ativo:
            raise ValueError("Usuário inativo não pode abrir chamado.")

        chamado = Chamado(
            id=self._proximo_id,
            titulo=titulo,
            descricao=descricao,
            laboratorio=laboratorio,
            prioridade=prioridade,
            autor=autor,
        )
        chamado.adicionar_historico("Chamado aberto.", autor)

        self._chamados.append(chamado)
        self._proximo_id += 1
        return chamado

    def listar_chamados(self, usuario: Usuario) -> list[Chamado]:
        if usuario.perfil in {Perfil.TECNICO, Perfil.ADMINISTRADOR}:
            return list(self._chamados)

        return [chamado for chamado in self._chamados if chamado.autor.id == usuario.id]


if __name__ == "__main__":
    aluno = Usuario(
        id=1,
        nome="Ana Souza",
        email="ana@faculdade.edu.br",
        perfil=Perfil.USUARIO,
    )

    tecnico = Usuario(
        id=2,
        nome="Carlos Lima",
        email="carlos@faculdade.edu.br",
        perfil=Perfil.TECNICO,
    )

    sistema = SistemaChamados()

    chamado = sistema.abrir_chamado(
        titulo="Computador não liga",
        descricao="A máquina 12 do laboratório 3 não está ligando.",
        laboratorio="Laboratório 3",
        prioridade=Prioridade.ALTA,
        autor=aluno,
    )

    chamado.alterar_status(Status.EM_ATENDIMENTO, tecnico)

    print(f"Chamado #{chamado.id}: {chamado.titulo}")
    print(f"Status atual: {chamado.status.value}")
    print("Histórico:")
    for item in chamado.historico:
        print(f"- {item.criado_em:%d/%m/%Y %H:%M} | {item.autor.nome}: {item.mensagem}")