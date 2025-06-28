from jobs.base_job import BaseJob


class SimpleJobScheduler:

    def __init__(self, web3_provider, exporters):
        self.web3_provider = web3_provider
        self.exporters = exporters
        self.jobs = []

    def register_job(self, job_class):
        """手动注册作业类"""
        job = job_class(
            web3_provider=self.web3_provider,
            exporters=self.exporters
        )

        self.jobs.append(job)

    def run_jobs(self, start_block, end_block):
        """按注册顺序执行作业"""
        self.clear_data_buff()

        print(f"开始执行作业序列: {start_block} - {end_block}")
        for job in self.jobs:
            print(f"execute job: {job.__class__.__name__}")
            print(f"当前 data_buff 内容: {list(BaseJob.data_buff.keys())}")
            print(f"当前 data_buff 内容: {BaseJob.data_buff.get('Block')}")
            job.run(start_block=start_block, end_block=end_block)

        # 输出统计信息
        print("\n=== 数据统计 ===")
        for job in self.jobs:
            for output_type in job.output_types:
                count = BaseJob.data_buff.get(output_type.type(), [])
                print(f"output type: {output_type}, {len(count)} records")

    @staticmethod
    def clear_data_buff():
        """清空数据缓冲区"""
        BaseJob.data_buff.clear()
