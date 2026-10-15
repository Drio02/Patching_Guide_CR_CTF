# Sinatra + Sequel / ActiveRecord

# Vuln 1: interpolacion en Sequel
post '/login' do
  user = DB["SELECT * FROM users WHERE username = '#{params[:username]}' AND password = '#{params[:password]}'"].first
  halt 401 unless user          # payload: admin' --
  session[:user] = user[:username]
end

# Vuln 2: interpolacion en un where de ActiveRecord
get '/notes' do
  Note.where("owner = '#{params[:owner]}'").to_json
end

# Vuln 3: order con input del usuario
get '/list' do
  Note.order(params[:sort]).to_json
end
