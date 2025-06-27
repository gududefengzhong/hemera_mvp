class SimpleJobScheduler:
    def __init__(self, web3_provider, exporters):
        self.web3_provider = web3_provider
        self.exporters = exporters
        self.jobs = []
        self.data_buff = {}

    def register_job(self, job_class):
        """手动注册作业类"""
        job = job_class(
            web3_provider=self.web3_provider,
            exporters=self.exporters,
            data_buff=self.data_buff,
        )

        self.jobs.append(job)

    def run_jobs(self, start_block, end_block):
        """按注册顺序执行作业"""
        self.clear_data_buff()

        for job in self.jobs:
            print(f"execute job: {job.__class__.__name__}")
            job.run(start_block=start_block, end_block=end_block)

        # 输出统计信息
        for job in self.jobs:
            for output_type in job.output_types:
                count = self.data_buff.get(output_type.type(), [])
                print(f"output type: {output_type}, {count} records")

    def clear_data_buff(self):
        """清空数据缓冲区"""
        self.data_buff.clear()
