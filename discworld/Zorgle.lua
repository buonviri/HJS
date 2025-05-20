function printmylist(x)

-- this function parses and prints a list of items separated by commas and ending with ... ",x and y"

-- set max count to be displayed
maxcount = 40

-- get string between colon and period
csv = x
csv = string.gsub(csv,"gold and mahogany","gold-and-mahogany")

-- convert to table and get count
t = utils.split (csv, ",")
tcount = table.getn(t)

-- break last table entry up, should have the format "x and y", unpredictable if x or y also contains the word 'and'
i = string.find(t[tcount]," and ")
if i ~= nil then -- found the first and hopefully only instance of " and "
   valuea = string.sub(t[tcount],1,i-1):match "^%s*(.-)%s*$"
   valueb = string.sub(t[tcount],i+5):match "^%s*(.-)%s*$"
   t[tcount] = valuea  -- replace x and y with x
   table.insert(t, valueb) -- append y
end

-- initialize
itemcount = 0
short_list = "\n"
formatted_list = "\n"
money = 0

-- list of item names to be shortened
short =
   {
   ["some fine grey ash"]                  = "TPA+",
   ["some fine white ash"]                 = "TPA+",
   ["a small leather shield"]              = "TPA-",
   ["a jagged coral dirk"]                 = "WEP",
   ["a rasher of extra-crispy bacon"]      = "WEP",
   ["two jagged coral dirks"]              = "WEP WEP",
   ["two rashers of extra-crispy bacon"]   = "WEP WEP",
   ["a gold-and-mahogany ring"]            = "NIK",
   ["a pair of iron gauntlets"]            = "STR",
   ["a crowbar"]                           = "JOB",
   ["a brass feather"]                     = "HAT",
   ["two brass feathers"]                  = "HAT",
   ["three brass feathers"]                = "HAT",
   ["a holy amulet"]                       = "HAT",
   ["a purple baton"]                      = "HAT",
   ["a ribboned baton"]                    = "HAT",
   ["a set of prayer beads"]               = "HAT",
   ["a ribbon charm bracelet"]             = "HAT",

   ["a black velvet bag"]                  = "BAG",
   ["a turnip sack"]                       = "BAG",
   ["a black bear fur-lined hat"]          = "OLD",
   ["a midnight black latex catsuit"]      = "CAT",
   ["a Thieves' Guild Licence"]            = "LIC",
   ["a deerskin Thieves' Guild licence"]   = "LIC",
   ["a club badge"]                        = "ROG",
   ["two club badges"]                     = "R+S",
   ["a red badge"]                         = "APX",
   ["a small canteen"]                     = "CAN",

   ["end of short list"] = "none"
   }

-- list of coin strings
coins =
   {
   ["rk royals"] = "royal",
   ["ork royal"] = "royal",
   ["lf-dollar"] = "half",
   ["f-dollars"] = "half",
   ["en-dollar"] = "ten",
   ["n-dollars"] = "ten",
   ["k dollars"] = "one",
   ["rk dollar"] = "one",
   ["ten-pence"] = "tp",
   ["ork pence"] = "p",
   ["ork penny"] = "p",
   ["end of coin list"] = "none"
   }

-- list of numerals
numeral =
   {
   ["a"]         =  "1",
   ["an"]        =  "1",
   ["one"]       =  "1",
   ["two"]       =  "2",
   ["three"]     =  "3",
   ["four"]      =  "4",
   ["five"]      =  "5",
   ["six"]       =  "6",
   ["seven"]     =  "7",
   ["eight"]     =  "8",
   ["nine"]      =  "9",
   ["ten"]       = "10",
   ["eleven"]    = "11",
   ["twelve"]    = "12",
   ["thirteen"]  = "13",
   ["fourteen"]  = "14",
   ["fifteen"]   = "15",
   ["sixteen"]   = "16",
   ["seventeen"] = "17",
   ["eighteen"]  = "18",
   ["nineteen"]  = "19",
   ["twenty"]    = "20",
   ["many"]      = "20+",
   ["end of list"] = "none"
   }

-- loop thru all items in table
for key, value in pairs(t) do
   ending = "\n"
   itemcount = itemcount + 1
   value = value:match "^%s*(.-)%s*$"
   if short[value] ~= nil then  -- string is in list of short names
      value = short[value]
      short_list = short_list .. " " .. value
   else -- string not in list, try checking tail
      tail = string.sub(value,string.len(value)-8)  -- last nine characters to look for currency
      if coins[tail] ~= nil then
         value = "" -- suppress string
         ending = "" -- don't add CRLF
         money = money + 1 -- increment money counter for summary at the end
      elseif tail == "ing paper" then -- special case, add to short list
         n = value:match("^(%S+)") -- get first word
         value = "" -- suppress string
         ending = "" -- don't add CRLF
         short_list = short_list .. " TPA[" .. numeral[n] .. "]"
      elseif tail == "parchment" then -- special case, add to short list
         n = value:match("^(%S+)") -- get first word
         value = "" -- suppress string
         ending = "" -- don't add CRLF
         short_list = short_list .. " TPA[" .. numeral[n] .. "]"
      elseif tail == "ack cloth" then -- special case, strips
         n = value:match("^(%S+)") -- get first word
         value = "" -- suppress string
         ending = "" -- don't add CRLF
         short_list = short_list .. " BAN[" .. numeral[n] .. "]"
      end
      if itemcount < maxcount then -- set max lines
--       if string.sub(value,0,4) == "five" or string.sub(value,0,3) == "six" or string.sub(value,0,4) == "some" or string.sub(value,0,5) == "seven" or string.sub(value,0,8) == "one pint" or string.sub(value,0,9) == "two pints" then
--          formatted_list = formatted_list .. " - " .. value .. ending -- add indent for five/six/seven/some/pint (removed 2025-05-19)
         if string.sub(value,0,12) == "a smuggler's" or string.sub(value,0,12) == "some smuggle" or string.sub(value,0,12) == "a pair of sm" or string.sub(value,0,12) == "a gold neckl" then
            formatted_list = formatted_list .. " " .. value .. ending -- smuggler's set and permalight, indent one
         else
            formatted_list = formatted_list .. value .. ending -- no indent
         end
      end
   end
end

-- add money if any was found
if money > 0 then
   formatted_list = formatted_list .. "\n(money: " .. money .. ")"
end

-- add short list if it's not still just "\n"
if string.len(short_list) > 1 then
   formatted_list = formatted_list .. short_list .. "\n" -- add list of short names
end

-- add elipses if truncated
if itemcount >= maxcount then
   formatted_list = formatted_list .. "...\n"
end

-- print list
print(formatted_list)

end

function printmyjob(a,b,c)

-- This function gets called for jobs such as:
-- You are required to deliver a pair of dentist's trousers to Fred Sylver at Sylver's on Washer Way.

-- needed for Quow interface
require "json"

-- print info directly to game window
print("   " .. a)
print("   " .. b)
print("   " .. c)
-- SetStatus(a.." --- "..b.." --- "..c) -- doesn't work, gets overwritten instantly by quota plugin

-- generate fake chat message
sForQuow = "Deliver \""..a.."\" to "..b.." ("..c..")"

 -- ColourNameToRGB("cornflowerblue") and royal weren't quite right, used Custom Color 5 from mushclient, click on Lua button to code decimal value
jobStyles = {[1] = {["textcolour"] = 16744448, ["backcolour"] = 0, ["text"] = sForQuow, ["length"] = string.len(sForQuow)}}

-- send to comms plugin
CallPlugin ("bfe35205f026786ea1d56e3b", "HandleExternalComms", json.encode({"Tells_In", sForQuow, jobStyles}))

end

function printmybank(a)

-- print to confirm amount
print("   " .. a .. " written to file.")

-- write to file
f = io.open( "./bank.txt", "a")
f:write(os.date("%y/%m/%d-%H:%M") .. " -> " .. a .. "\n")
f:close()

end

function printmysausage(a,b,c)

-- This function gets called for jobs such as:
-- You have four hours to deliver 75 fresh sheep sausages to Sam Slager.

-- needed for Quow interface
require "json"

-- print info directly to game window (overkill for sausage missions)
-- print("   " .. a)
-- print("   " .. b)
-- print("   " .. c)
-- SetStatus(a.." --- "..b.." --- "..c) -- doesn't work, gets overwritten instantly by quota plugin

-- generate fake chat message
sForQuow = "Deliver "..b.." sausages to "..c

 -- ColourNameToRGB("cornflowerblue") and royal weren't quite right, used Custom Color 5 from mushclient, click on Lua button to code decimal value
jobStyles = {[1] = {["textcolour"] = 16744448, ["backcolour"] = 0, ["text"] = sForQuow, ["length"] = string.len(sForQuow)}}

-- send to comms plugin
CallPlugin ("bfe35205f026786ea1d56e3b", "HandleExternalComms", json.encode({"Tells_In", sForQuow, jobStyles}))

end
