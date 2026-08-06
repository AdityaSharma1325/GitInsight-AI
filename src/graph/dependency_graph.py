from pathlib import Path
import ast
from pyvis.network import Network


def extract_imports(file_path):
    """
    Return imported modules from a Python file.
    """

    imports = []

    try:
        code = Path(file_path).read_text(
            encoding="utf-8",
            errors="ignore"
        )

        tree = ast.parse(code)

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):

                for alias in node.names:
                    imports.append(alias.name)

            elif isinstance(node, ast.ImportFrom):

                if node.module:
                    imports.append(node.module)

    except Exception:
        pass

    return imports


def build_dependency_graph(repo_path):
    """
    Build a graph of Python file dependencies.
    """

    repo_path = Path(repo_path)

    graph = {}

    for file in repo_path.rglob("*.py"):

        graph[file.name] = extract_imports(file)

    return graph


def visualize_graph(graph):

    net = Network(
        height="700px",
        width="100%"
    )

    for file, imports in graph.items():

        net.add_node(file, color="lightblue")

        for module in imports:

            net.add_node(module)

            net.add_edge(file, module)

    net.save_graph("dependency_graph.html")

    return "dependency_graph.html"