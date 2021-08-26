cwlVersion: v1.0
class: CommandLineTool
hints:
  DockerRequirement:
    dockerPull: trinityrnaseq/trinityrnaseq:2.13.1
requirements:
  - class: InlineJavascriptRequirement
  - class: InitialWorkDirRequirement
    listing:
      - $(inputs.fq1)
      - $(inputs.fq2)
baseCommand: ["/usr/local/bin/trinityrnaseq/util/align_and_estimate_abundance.pl"]

inputs:
  seq_type: 
    type: string
    inputBinding:
      position: 1
      prefix: --seqType
  max_memory:
    type: string
    inputBinding:
      position: 2
      prefix: --max_memory
  fq1:
    type: File
    inputBinding:
      position: 3
      prefix: --left
      valueFrom: $(self.basename)
  fq2:
    type: File
    inputBinding:
      position: 4
      prefix: --right
      valueFrom: $(self.basename)
  threads:
    type: int?
    inputBinding:
      position: 5
      prefix: --thread_count
  transcript_name:
    type: File
    inputBinding:
      position: 6
      prefix: --transcripts
      valueFrom: $(self.basename)
  estmethod: 
    type: string
    inputBinding:
      position: 7
      prefix: --est_method
  salmonaddopts: 
    type: string
    inputBinding:
      position: 8
      prefix: --salmon_add_opts
  prep_ref:
    type: string
    inputBinding:
      position: 9
      prefix: --prep_reference
outputs:
  trinity_results:
    type: Directory
    outputBinding:
      glob: $(inputs.output_dir)

$namespaces:
  s: https://schema.org/
  edam: http://edamontology.org/

s:license: https://spdx.org/licenses/Apache-2.0
s:codeRepository: https://github.com/pitagora-network/pitagora-cwl

$schemas:
  - https://schema.org/docs/schema_org_rdfa.html
  - http://edamontology.org/EDAM_1.18.owl
