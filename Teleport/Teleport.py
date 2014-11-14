__author__ = 'M0rdreck'
__version__ = '1.1'

import clr
import sys
import math
clr.AddReferenceByPartialName("UnityEngine")
clr.AddReferenceByPartialName("Pluton")
import UnityEngine
import Pluton
import System

class Teleport:
    def config(self):
        if(Plugin.IniExists("teleport")):
            return Plugin.GetIni("teleport")
        else:
            Plugin.CreateIni("teleport")
            ini = Plugin.GetIni("teleport")
            ini.AddSetting("config","language","en")
            ini.AddSetting("config","home","1")
            ini.AddSetting("config","nbhome","1")
            ini.AddSetting("config","tp","1")
            ini.AddSetting("config","delay","3600")
            ini.AddSetting("config","nb","2")

    def infos(self):
        if(Plugin.IniExists("teleportInfos")):
            return Plugin.GetIni("teleportInfos")
        else:
            Plugin.CreateIni("teleportInfos")
            ini = Plugin.GetIni("teleportInfos")

    def home(self):
        if(Plugin.IniExists("teleportHome")):
            return Plugin.GetIni("teleportHome")
        else:
            Plugin.CreateIni("teleportHome")
            return Plugin.GetIni("teleportHome")

    def language(self):
        if (Plugin.IniExists("teleportLanguage")):
            return Plugin.GetIni("teleportLanguage")
        else:
            Plugin.CreateIni("teleportLanguage")
            return Plugin.Getini("teleportLanguage")

    def nbTeleport(self, gid):
        if iniInfos.GetSetting(str(gid), "nombre") != "" and iniInfos.GetSetting(str(gid), "nombre") is not None:
            return iniInfos.GetSetting(str(gid), "nombre")

    def delaisTeleport(self, gid):
        if iniInfos.GetSetting(str(gid), "delais") != "" and iniInfos.GetSetting(str(gid), "delais") is not None:
            return iniInfos.GetSetting(str(gid), "delais")

    def setGlobal(self, key, value):
        g = globals()
        g[key] = value

    def getGlobal(self, key):
        g = globals()
        if key in g:
            return g[key]
        else:
            return None

    def On_PluginInit(self):
        global iniConfig
        iniConfig = self.config()
        global teleportRequest
        teleportRequest = {}
        global iniInfos
        iniInfos = self.infos()
        global iniHome
        iniHome = self.home()
        global iniLang
        iniLang = self.language()
        Commands.Register("teleportconfig")\
            .setCallback(self.cmdConfig)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "description_config_list"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "usage_config_list"))
        Commands.Register("teleportconfigupdate")\
            .setCallback(self.cmdConfigUpdate)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "description_config_update"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "usage_config_update"))
        Commands.Register("listhome")\
            .setCallback(self.cmdListHome)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "description_home_list"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "usage_home_list"))
        Commands.Register("addhome")\
            .setCallback(self.cmdAddHome)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "description_home_add"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "usage_home_add"))
        Commands.Register("delhome")\
            .setCallback(self.cmdDelHome)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "description_home_del"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "usage_home_del"))
        Commands.Register("tphome")\
            .setCallback(self.cmdTpHome)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "description_home_tp"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "usage_home_tp"))
        Commands.Register("tplist")\
            .setCallback(self.cmdTpList)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "description_tp_list"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "usage_tp_list"))
        Commands.Register("tp")\
            .setCallback(self.cmdTp)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "description_tp"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "usage_tp"))
        Commands.Register("tpa")\
            .setCallback(self.cmdTpAccept)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "description_tp_accept"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "usage_tp_accept"))
        Commands.Register("tpr")\
            .setCallback(self.cmdTpRefuse)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "description_tp_refuse"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "usage_tp_refuse"))
        Commands.Register("tpa")\
            .setCallback(self.cmdAdminTp)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "description_admin_tp"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "usage_admin_tp"))
        Commands.Register("tploc")\
            .setCallback(self.cmdAdminTpLoc)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "description_admin_tp_loc"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "usage_admin_tp_loc"))


    def cmdConfig(self, args, player):
        if not player.Admin:
            return
        enum = iniConfig.EnumSection("Config")
        player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "config_titre_liste"))
        for key in enum:
            player.Message(str(key) + " = " + iniConfig.GetSetting("Config", key))
        player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "config_how_to"))

    def cmdConfigUpdate(self, args, player):
        if not player.Admin:
            return
        config = iniConfig.GetSetting("Config", str(args[0]))
        if(config != "" and config is not None):
            iniConfig.AddSetting("Config", str(args[0]), str(args[1]))
            player.Message(str(args[0]) + " = " + str(args[1]))
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "config_update"))
        else:
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "config_not_found"))

    def cmdListHome(self, args, player):
        quotedargs = Util.GetQuotedArgs(args)
        gid = str(player.GameID)
        player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "home_list"))
        enum = iniHome.EnumSection(gid)
        n = 0
        for key in enum:
            player.Message(n + ". " + key)
            n=n+1

    def cmdAddHome(self, args, player):
        quotedargs = Util.GetQuotedArgs(args)
        gid = str(player.GameID)
        loc = str(player.X) + "/" + str(player.Y) + "/" + str(player.Z)
        if iniHome.GetSetting(gid, quotedargs[0]) != "" and iniHome.GetSetting(gid, args[0]) is not None:
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "home_exists").replace("[[name]]", quotedargs[0]))
            return
        else:
            iniHome.AddSetting(gid, quotedargs[0], loc)
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "home_create").replace("[[name]]", quotedargs[0]))
            return

    def cmdDelHome(self, args, player):
        quotedargs = Util.GetQuotedArgs(args)
        gid = str(player.GameID)
        loc = str(player.X) + "/" + str(player.Y) + "/" + str(player.Z)
        if iniHome.GetSetting(gid, quotedargs[0]) != "" and iniHome.GetSetting(gid, quotedargs[0]) is not None:
            iniHome.DelSetting(gid, quotedargs[0])
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "home_delete").replace("[[name]]", quotedargs[0]))
            return
        else:
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "home_not_found").replace("[[name]]", quotedargs[0]))
            return

    def cmdTpHome(self, args, player):
        quotedargs = Util.GetQuotedArgs(args)
        gid = str(player.GameID)
        time = Plugin.GetTimestamp()
        nombreMax = iniConfig.GetSetting("Config", "nb")
        delaisMax = float(iniConfig.GetSetting("Config", "delais")) * 1000
        delais = int(delaisTeleport(gid)) + int(delaisMax)
        nombre = nbTeleport(gid)
        if iniHome.GetSetting(gid, quotedargs[0]) != "" and iniHome.GetSetting(gid, args[0]) is not None:
            loc = iniHome.GetSetting(gid, quotedargs[0]).split('/')
        else:
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "home_not_found").replace("[[name]]", quotedargs[0]))
            return
        if nombre == nombreMax:
            p.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "max_tp").replace("[[nb]]", nombreMax))
            del teleportRequest[str(gidFrom)]
            return
        if delais > time:
            p.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "delais_tp").replace("[[delais]]", delaisMax))
            del teleportRequest[str(gidFrom)]
            return
        playerFrom.GroundTeleport(float(loc[0]), float(loc[1]), float(loc[2]))
        playerFrom.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "teleport_to_home").replace("[[home]]", quotedargs[0]))

    def cmdTp(self, args, player):
        quotedargs = Util.GetQuotedArgs(args)
        gid = str(player.GameID)
        time = Plugin.GetTimestamp()
        nombreMax = iniConfig.GetSetting("Config", "nb")
        delaisMax = float(iniConfig.GetSetting("Config", "delais")) * 1000
        delais = int(delaisTeleport(gid)) + int(delaisMax)
        nombre = nbTeleport(gid)
        if nombre == nombreMax:
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "max_tp").replace("[[nb]]", nombreMax))
            return
        if delais > time:
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "delais_tp").replace("[[delais]]", delaisMax))
            return
        for p in Server.ActivePlayers:
            if(p.Name.lower() == quotedArgs[0].lower()):
                if teleportRequest.has_key(str(player.GameID)):
                    teleportRequest[str(player.GameID)][str(p.GameID)] = 1
                else:
                    teleportRequest[str(player.GameID)] = {}
                    teleportRequest[str(player.GameID)][str(p.GameID)] = 1
                p.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "tp_requete").replace("[[name]]", player.Name))

    def cmdTpAccept(self, args, player):
        quotedargs = Util.GetQuotedArgs(args)
        gid = str(player.GameID)
        time = Plugin.GetTimestamp()
        nombreMax = iniConfig.GetSetting("Config", "nb")
        delaisMax = float(iniConfig.GetSetting("Config", "delais")) * 1000
        playerFrom = None
        gidFrom = None
        for p in Server.ActivePlayers:
            if p.Name.lower() == quotedArgs[0].lower():
                playerFrom = p
                gidFrom = str(p.GameID)
        if gidFrom == None:
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "player_not_found").replace('[[user]]', quotedargs[0]))
            return
        if teleportRequest.has_key(str(gidFrom)):
            t = teleportRequest[str(gidFrom)]
            if t.has_key(str(gid)) == False:
                player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "no_tp_request_found"))
                return
        else:
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "no_tp_request_found"))
            return
        delais = int(delaisTeleport(gidFrom)) + int(delaisMax)
        nombre = nbTeleport(gidFrom)
        if nombre == nombreMax:
            playerFrom.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "max_tp").replace("[[nb]]", nombreMax))
            del teleportRequest[str(gidFrom)]
            return
        if delais > time:
            playerFrom.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "delais_tp").replace("[[delais]]", delaisMax))
            del teleportRequest[str(gidFrom)]
            return
        playerFrom.GroundTeleport(float(playerFrom.X), float(playerFromp.y), float(playerFrom.z))
        playerFrom.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "teleport_to").replace("[[user]]", player.Name))

    def cmdTpRefuse(self, args, player):
        quotedargs = Util.GetQuotedArgs(args)
        gid = str(player.GameID)
        playerFrom = None
        gidFrom = None
        for p in Server.ActivePlayers:
            if(p.Name.lower() == quotedArgs[0].lower()):
                playerFrom = p
                gidFrom = str(p.GameID)
        if gidFrom == None:
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "player_not_found").replace('[[user]]', quotedargs[0]))
            return
        if teleportRequest.has_key(str(gidFrom)):
            t = teleportRequest[str(gidFrom)]
            if t.has_key(str(gid)):
                playerFrom.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "teleport_no_accept").replace("[[user]]", player.Name))
                del teleportRequest[str(gidFrom)][str(gid)]
                return

    def cmdTpList(self, args, player):
        quotedargs = Util.GetQuotedArgs(args)
        gid = str(player.GameID)
        playerFrom.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "teleport_list_request"))
        if teleportRequest.has_key(str(gid)):
            enum = teleportRequest.EnumSection(gid)
            n = 0
            for key in enum:
                for p in Server.ActivePlayers:
                    if(str(p.GameID) == key):
                        playerFrom.Message(n + ". " + p.Name)
                        n = n + 1
                for p in Server.SleepingPlayers:
                    if(str(p.GameID) == key):
                        playerFrom.Message(n + ". " + p.Name)
                        n = n + 1

    def cmdAdminTp(self, args, player):
        quotedargs = Util.GetQuotedArgs(args)
        gid = str(player.GameID)
        if not player.Admin:
            return
        for p in Server.ActivePlayers:
            if(p.Name.lower() == cmd.quotedArgs[0].lower()):
                player.GroundTeleport(p.X, p.Y, p.Z)
                player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "teleport_to_").replace("[[user]]", quotedargs[0]))
                p.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "admin_teleport").replace("[[user]]", player.Name))
                return
        for p in Server.SleepingPlayers:
            if(p.Name.lower() == cmd.quotedArgs[0].lower()):
                player.GroundTeleport(p.X, p.Y, p.Z)
                player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "teleport_to_").replace("[[user]]", quotedargs[0]))
                return
        player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "player_not_found").replace('[[user]]', quotedargs[0]))

    def cmdAdminTpLoc(self, args, player):
        quotedargs = Util.GetQuotedArgs(args)
        player.GroundTeleport(float(quotedargs[0]), float(quotedargs[1]), float(quotedargs[2]))
        player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "teleport_to_pos").replace("[[loc]]", "X=" + str(quotedargs[0]) + " Y=" + str(quotedargs[1]) + " Z=" + str(quotedargs[2])))