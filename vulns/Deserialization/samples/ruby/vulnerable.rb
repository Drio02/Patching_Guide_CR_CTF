# Sinatra
require 'base64'
require 'yaml'

# Vuln 1: Marshal.load de una cookie (gadget chains universales para Ruby 2.x/3.x)
get '/dashboard' do
  prefs = Marshal.load(Base64.decode64(request.cookies['prefs']))
  "theme: #{prefs[:theme]}"
end

# Vuln 2: YAML.load con Psych < 4 instancia objetos arbitrarios
post '/import' do
  cfg = YAML.load(request.body.read)
  cfg.to_s
end
