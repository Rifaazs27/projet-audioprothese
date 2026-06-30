{{- define "audioprothese.backendImage" -}}
{{- if .Values.image.registry -}}
{{ .Values.image.registry }}/{{ .Values.image.backendRepository }}:{{ .Values.image.tag }}
{{- else -}}
{{ .Values.image.backendRepository }}:{{ .Values.image.tag }}
{{- end -}}
{{- end -}}

{{- define "audioprothese.frontendImage" -}}
{{- if .Values.image.registry -}}
{{ .Values.image.registry }}/{{ .Values.image.frontendRepository }}:{{ .Values.image.tag }}
{{- else -}}
{{ .Values.image.frontendRepository }}:{{ .Values.image.tag }}
{{- end -}}
{{- end -}}

{{- define "audioprothese.labels" -}}
app.kubernetes.io/name: audioprothese
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}
