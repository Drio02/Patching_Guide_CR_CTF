# Sinatra
require 'ipaddr'
require 'open3'

# Patch 1: Open3 con varios argumentos (sin shell) + validacion de IP
post '/ping' do
  host = IPAddr.new(params[:host].to_s).to_s rescue halt(400)
  out, _status = Open3.capture2e('ping', '-c', '1', host)
  out
end

# Patch 2: system con varios argumentos + nombre validado
get '/archive' do
  dir = params[:dir].to_s
  halt 400 unless dir.match?(/\A[A-Za-z0-9_-]{1,64}\z/)
  system('tar', 'czf', '/tmp/out.tgz', '--', "notes/#{dir}")
  send_file '/tmp/out.tgz'
end

# Patch 3: File.read nunca interpreta "|" (Kernel#open si)
get '/read' do
  name = File.basename(params[:file].to_s)
  File.read(File.join('notes', name))
end
