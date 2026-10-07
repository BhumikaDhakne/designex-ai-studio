from collections import defaultdict

from backend.app.schemas.project import Project


class DependencyService:
    """Calculates deterministic task dependency relationships."""

    def __init__(self, project: Project):
        self.project = project

        self.valid_task_ids = {
            task.task_id
            for task in project.tasks
        }

        self.downstream_map: dict[str, list[str]] = defaultdict(list)

        for dependency in project.task_dependencies:
            self.downstream_map[
                dependency.depends_on_task_id
            ].append(dependency.task_id)

    def normalize_task_id(self, task_reference: str) -> str | None:
        """
        Resolve a task reference to a valid project task ID.

        Supports both:
        - T-002
        - T-002 - Update BOQ for marble works
        """

        reference = task_reference.strip()

        if reference in self.valid_task_ids:
            return reference

        for task_id in self.valid_task_ids:
            if reference.startswith(f"{task_id} "):
                return task_id

            if reference.startswith(f"{task_id}-"):
                return task_id

        return None

    def get_direct_downstream_tasks(
        self,
        task_id: str,
    ) -> list[str]:
        """Return tasks that directly depend on the given task."""

        normalized_task_id = self.normalize_task_id(task_id)

        if normalized_task_id is None:
            return []

        return self.downstream_map.get(
            normalized_task_id,
            [],
        ).copy()

    def get_all_downstream_tasks(
        self,
        task_id: str,
    ) -> list[str]:
        """
        Return every task downstream of the given task.

        Traversal continues through the complete dependency chain.
        """

        normalized_task_id = self.normalize_task_id(task_id)

        if normalized_task_id is None:
            return []

        visited: set[str] = set()

        queue = list(
            self.get_direct_downstream_tasks(
                normalized_task_id
            )
        )

        while queue:
            current_task = queue.pop(0)

            if current_task in visited:
                continue

            visited.add(current_task)

            queue.extend(
                self.get_direct_downstream_tasks(
                    current_task
                )
            )

        return self._order_tasks_as_project_dependencies(
            visited
        )

    def _order_tasks_as_project_dependencies(
        self,
        task_ids: set[str],
    ) -> list[str]:
        """Return task IDs in the project's task order."""

        project_task_order = [
            task.task_id
            for task in self.project.tasks
        ]

        return [
            task_id
            for task_id in project_task_order
            if task_id in task_ids
        ]