export type Status = 'MET' | 'PARTIAL' | 'NOT_EVIDENCED' | 'CONTRADICTED'
export type Decision = 'pending' | 'shortlisted' | 'talk_first' | 'rejected'
export interface Finding { id: string; category: string; requirement: string; status: Status; reason: string; quote?: string; source?: string }
export const findings: Finding[] = [
  { id:'req-aws', category:'Required skills', requirement:'Hands-on AWS experience', status:'MET', reason:'Production infrastructure ownership is directly evidenced.', quote:'Designed and operated multi-account AWS environments using Terraform.', source:'Resume · Experience · paragraph 2' },
  { id:'req-iac', category:'Required skills', requirement:'Infrastructure as code', status:'MET', reason:'Terraform usage is explicit and applied.', quote:'Reduced provisioning time by 60% through reusable Terraform modules.', source:'Resume · Experience · paragraph 3' },
  { id:'req-exp', category:'Relevant experience', requirement:'4+ years in cloud engineering', status:'PARTIAL', reason:'Grounded month-level intervals establish 38 months; earlier duration is unclear.', quote:'Cloud Engineer · Mar 2023 – Present', source:'Resume · Experience · paragraph 1' },
  { id:'req-k8s', category:'Responsibilities', requirement:'Own production Kubernetes workloads', status:'NOT_EVIDENCED', reason:'The resume does not establish Kubernetes production ownership.' },
  { id:'req-observe', category:'Responsibilities', requirement:'Build monitoring and incident response', status:'MET', reason:'Monitoring and on-call ownership are directly supported.', quote:'Built Grafana dashboards and led the weekly on-call rotation.', source:'Resume · Experience · paragraph 4' },
  { id:'req-python', category:'Preferred skills', requirement:'Python automation', status:'PARTIAL', reason:'Python scripting is present; the confirmed rubric requires a production example.', quote:'Automated operational checks with Python and Bash.', source:'Resume · Skills · paragraph 1' },
]
export const stages = ['Queued', 'Extracting', 'Analyzing', 'Validating', 'Scoring', 'Ready']
