from sqlalchemy import create_engine

class CommitSqlPipeline(object):
	def __init__(self):
		self.engine = create_engine("sqlite:///data.db")

	def process_item(self, item, spider):
		try:
			item.commit_item(engine=self.engine)
		except:
			print('Duplicate Entry found in DB')
