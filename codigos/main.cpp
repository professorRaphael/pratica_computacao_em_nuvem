#include <iostream>
#include <string>
#include <vector>
#include <stdexcept>

enum class Perfil {
    Usuario,
    Tecnico,
    Administrador
};

enum class Prioridade {
    Baixa,
    Media,
    Alta
};

enum class Status {
    Aberto,
    EmAtendimento,
    Resolvido,
    Cancelado
};

std::string statusParaTexto(Status status) {
    switch (status) {
        case Status::Aberto:
            return "Aberto";
        case Status::EmAtendimento:
            return "Em atendimento";
        case Status::Resolvido:
            return "Resolvido";
        case Status::Cancelado:
            return "Cancelado";
        default:
            return "Desconhecido";
    }
}

class Usuario {
private:
    int id;
    std::string nome;
    std::string email;
    Perfil perfil;

public:
    Usuario(int id, std::string nome, std::string email, Perfil perfil)
        : id(id), nome(std::move(nome)), email(std::move(email)), perfil(perfil) {}

    int getId() const {
        return id;
    }

    std::string getNome() const {
        return nome;
    }

    Perfil getPerfil() const {
        return perfil;
    }
};

class Chamado {
private:
    int id;
    std::string titulo;
    std::string descricao;
    std::string laboratorio;
    Prioridade prioridade;
    Status status;
    Usuario autor;
    std::vector<std::string> historico;

public:
    Chamado(
        int id,
        std::string titulo,
        std::string descricao,
        std::string laboratorio,
        Prioridade prioridade,
        Usuario autor
    )
        : id(id),
          titulo(std::move(titulo)),
          descricao(std::move(descricao)),
          laboratorio(std::move(laboratorio)),
          prioridade(prioridade),
          status(Status::Aberto),
          autor(std::move(autor)) {
        historico.push_back("Chamado aberto.");
    }

    void alterarStatus(Status novoStatus, const Usuario& usuario) {
        if (
            usuario.getPerfil() != Perfil::Tecnico &&
            usuario.getPerfil() != Perfil::Administrador
        ) {
            throw std::runtime_error("Somente técnico ou administrador pode alterar status.");
        }

        std::string mensagem = "Status alterado de " +
            statusParaTexto(status) + " para " + statusParaTexto(novoStatus) +
            " por " + usuario.getNome() + ".";

        status = novoStatus;
        historico.push_back(mensagem);
    }

    void imprimirResumo() const {
        std::cout << "Chamado #" << id << "\n";
        std::cout << "Título: " << titulo << "\n";
        std::cout << "Laboratório: " << laboratorio << "\n";
        std::cout << "Status: " << statusParaTexto(status) << "\n";
        std::cout << "Histórico:\n";

        for (const auto& item : historico) {
            std::cout << "- " << item << "\n";
        }
    }
};

int main() {
    Usuario aluno(
        1,
        "Ana Souza",
        "ana@faculdade.edu.br",
        Perfil::Usuario
    );

    Usuario tecnico(
        2,
        "Carlos Lima",
        "carlos@faculdade.edu.br",
        Perfil::Tecnico
    );

    Chamado chamado(
        1,
        "Computador não liga",
        "A máquina 12 do laboratório 3 não está ligando.",
        "Laboratório 3",
        Prioridade::Alta,
        aluno
    );

    chamado.alterarStatus(Status::EmAtendimento, tecnico);
    chamado.imprimirResumo();

    return 0;
}