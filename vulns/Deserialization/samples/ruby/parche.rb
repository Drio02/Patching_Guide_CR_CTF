# Sinatra
require 'base64'
require 'json'
require 'yaml'

# Patch 1: JSON en vez de Marshal
get '/dashboard' do
  prefs = JSON.parse(Base64.decode64(request.cookies['prefs'].to_s)) rescue halt(400)
  "theme: #{prefs['theme']}"
end

# Patch 2: safe_load solo permite tipos basicos
post '/import' do
  cfg = YAML.safe_load(request.body.read, permitted_classes: [], aliases: false)
  cfg.to_s
end
