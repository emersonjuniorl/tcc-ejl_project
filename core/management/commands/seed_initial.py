from django.core.management.base import BaseCommand
from core.models import Dimension, Question


class Command(BaseCommand):
	help = "Seed initial dimensions and questions"

	def handle(self, *args, **options):
		# Clear existing questions to ensure exact count
		Question.objects.all().delete()
		
		seeds = [
			(
				{"code": "PM_PLAN", "title": "Planejamento", "framework": "PMBOK"},
				[
					("Existe um plano de projeto formalmente aprovado?", 1.0),
					("O cronograma foi desenvolvido com estimativas confiáveis?", 1.0),
					("Os riscos foram identificados e possuem planos de resposta?", 1.0),
				],
			),
			(
				{"code": "HC_CHANGE", "title": "Gestão de Mudanças", "framework": "HCMBOK"},
				[
					("Há plano estruturado de gestão de mudanças?", 1.0),
					("Comunicação com stakeholders é contínua e segmentada?", 1.0),
				],
			),
			(
				{"code": "PR_GOV", "title": "Governança do Projeto", "framework": "PRINCE"},
				[
					("Papéis e responsabilidades estão claros?", 1.0),
					("Decisões e exceções são registradas e rastreáveis?", 1.0),
					("Há checkpoints/gates definidos e aplicados?", 1.0),
				],
			),
			(
				{"code": "COMP_CTRL", "title": "Controles de Compliance", "framework": "COMPLIANCE"},
				[
					("O projeto segue políticas e procedimentos internos?", 1.0),
					("Registros de compliance são mantidos e auditáveis?", 1.0),
				],
			),
		]

		created_dims = 0
		created_qs = 0
		for dim_data, questions in seeds:
			dim, created = Dimension.objects.get_or_create(**dim_data)
			if created:
				created_dims += 1
			for idx, (text, weight) in enumerate(questions, start=1):
				q, q_created = Question.objects.get_or_create(
					dimension=dim, text=text, defaults={"weight": weight, "order": idx}
				)
				if q_created:
					created_qs += 1

		total_questions = Question.objects.count()
		self.stdout.write(
			self.style.SUCCESS(
				f"Seed concluído: {created_dims} dimensões, {total_questions} questões criadas."
			)
		)


