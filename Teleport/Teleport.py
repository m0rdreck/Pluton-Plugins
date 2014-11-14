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
            ini.AddSetting("config","tpResquestDelay","60")
            ini.AddSetting("config","delay","3600")
            ini.AddSetting("config","delayBefore","10")
            ini.AddSetting("config", "PVPTime", "60")
            ini.AddSetting("config","nb","2")
            ini.AddSetting("config","rad","2")

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

    def On_PlayerAttacked(self, phe):
        player = phe.Victim
        time = Plugin.GetTimestamp()
        DataStore.Add("TeleportPVP", str(player.GameID), time)

    def On_PlayerTakeDamage(self, ptd):
        player = ptd.Victim
        time = Plugin.GetTimestamp()
        DataStore.Add("TeleportPVP", str(player.GameID), time)

    def On_PlayerTakeRads(self, ptr):
        player = ptr.Victim
        time = Plugin.GetTimestamp()
        DataStore.Add("TeleportPVP", str(player.GameID), time)

    def On_AllPluginsLoaded(self):
        global removePlugin
        removePlugin = Plugin.GetPlugin("Remove")

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
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "description_config_list"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "usage_config_list"))
        Commands.Register("teleportconfigupdate")\
            .setCallback(self.cmdConfigUpdate)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "description_config_update"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "usage_config_update"))
        Commands.Register("listhome")\
            .setCallback(self.cmdListHome)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "description_home_list"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "usage_home_list"))
        Commands.Register("addhome")\
            .setCallback(self.cmdAddHome)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "description_home_add"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "usage_home_add"))
        Commands.Register("delhome")\
            .setCallback(self.cmdDelHome)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "description_home_del"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "usage_home_del"))
        Commands.Register("tphome")\
            .setCallback(self.cmdTpHome)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "description_home_tp"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "usage_home_tp"))
        Commands.Register("tplist")\
            .setCallback(self.cmdTpList)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "description_tp_list"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "usage_tp_list"))
        Commands.Register("tp")\
            .setCallback(self.cmdTp)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "description_tp"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "usage_tp"))
        Commands.Register("tpa")\
            .setCallback(self.cmdTpAccept)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "description_tp_accept"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "usage_tp_accept"))
        Commands.Register("tpr")\
            .setCallback(self.cmdTpRefuse)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "description_tp_refuse"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "usage_tp_refuse"))
        Commands.Register("tpa")\
            .setCallback(self.cmdAdminTp)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "description_admin_tp"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "usage_admin_tp"))
        Commands.Register("tploc")\
            .setCallback(self.cmdAdminTpLoc)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "description_admin_tp_loc"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "usage_admin_tp_loc"))

    def TeleportCallback(self, timer):
        data = timer.Args
        p = data["Player"]
        p.GroundTeleport(float(data["X"]), float(data["Y"]), float(data["Z"]))
        p.Message(str(data["Message"]))
        timer.Kill()

    def TeleportRequestCallback(self, timer):
        data = timer.Args
        if teleportRequest.has_key(str(data["playerA"])):
            t = teleportRequest[str(data["playerA"])]
            if t.has_key(str(data["playerB"])):
                del teleportRequest[str(player.GameID)][str(p.GameID)]
        timer.Kill()

    def cmdSleeping(self, player):
        player.basePlayer.supressSnapshots = True
        player.basePlayer.UpdateNetworkGroup()
        player.basePlayer.UpdatePlayerCollider(True, False)
        player.basePlayer.SendFullSnapshot()
        player.basePlayer.inventory.SendSnapshot()

    def cmdConfig(self, args, player):
        if not player.Admin:
            return
        enum = iniConfig.EnumSection("Config")
        player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "config_titre_liste"))
        for key in enum:
            player.Message(str(key) + " = " + iniConfig.GetSetting("config", key) + "(" + iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "config_description_"+key) + ")")
        player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "config_how_to"))

    def cmdConfigUpdate(self, args, player):
        if not player.Admin:
            return
        config = iniConfig.GetSetting("config", str(args[0]))
        if(config != "" and config is not None):
            iniConfig.AddSetting("Config", str(args[0]), str(args[1]))
            player.Message(str(args[0]) + " = " + str(args[1]))
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "config_update"))
        else:
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "config_not_found"))

    def cmdListHome(self, args, player):
        if iniConfig.GetSetting("config", "home") == str(1):
            quotedargs = Util.GetQuotedArgs(args)
            gid = str(player.GameID)
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "home_list"))
            enum = iniHome.EnumSection(gid)
            n = 0
            for key in enum:
                player.Message(n + ". " + key)
                n += 1
        else:
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "home_not_activate"))

    def cmdAddHome(self, args, player):
        if iniConfig.GetSetting("config", "home") == str(1):
            quotedargs = Util.GetQuotedArgs(args)
            gid = str(player.GameID)
            loc = str(player.X) + "/" + str(player.Y) + "/" + str(player.Z)
            if iniHome.GetSetting(gid, quotedargs[0]) != "" and iniHome.GetSetting(gid, args[0]) is not None:
                player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "home_exists").replace("[[name]]", quotedargs[0]))
                return
            else:
                if removePlugin is not None:
                    loc = {}
                    loc[0] = player.X
                    loc[1] = player.Y
                    loc[2] = player.Z
                    r = remove.Invoke("searchBuilding", loc, gid, iniConfig.GetSetting("config", "rad"))
                    if r is not None and r == False:
                        player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "anti_home_raid"))
                        return
                iniHome.AddSetting(gid, quotedargs[0], loc)
                player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "home_create").replace("[[name]]", quotedargs[0]))
                return
        else:
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "home_not_activate"))

    def cmdDelHome(self, args, player):
        if iniConfig.GetSetting("config", "home") == str(1):
            quotedargs = Util.GetQuotedArgs(args)
            gid = str(player.GameID)
            loc = str(player.X) + "/" + str(player.Y) + "/" + str(player.Z)
            if iniHome.GetSetting(gid, quotedargs[0]) != "" and iniHome.GetSetting(gid, quotedargs[0]) is not None:
                iniHome.DelSetting(gid, quotedargs[0])
                player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "home_delete").replace("[[name]]", quotedargs[0]))
                return
            else:
                player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "home_not_found").replace("[[name]]", quotedargs[0]))
                return
        else:
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "home_not_activate"))

    def cmdTpHome(self, args, player):
        if iniConfig.GetSetting("config", "home") == str(1):
            quotedargs = Util.GetQuotedArgs(args)
            gid = str(player.GameID)
            time = Plugin.GetTimestamp()
            nombreMax = iniConfig.GetSetting("config", "nb")
            delaisMax = int(iniConfig.GetSetting("config", "delais")) * 1000
            delais = int(delaisTeleport(gid)) + int(delaisMax)
            nombre = nbTeleport(gid)
            if iniHome.GetSetting(gid, quotedargs[0]) != "" and iniHome.GetSetting(gid, args[0]) is not None:
                loc = iniHome.GetSetting(gid, quotedargs[0]).split('/')
            else:
                player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "home_not_found").replace("[[name]]", quotedargs[0]))
                return
            if nombre == nombreMax:
                p.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "max_tp").replace("[[nb]]", nombreMax))
                return
            if delais > time:
                p.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "delais_tp").replace("[[delais]]", iniConfig.GetSetting("config", "delais")))
                return
            if DataStore.ContainsKey("TeleportPVP", str(player.GameID)):
                pvpDelay = DataStore.ContainsKey("TeleportPVP", str(player.GameID))
                pvpTime = int(iniConfig.GetSettin("config","pvpTime")) * 1000
                delais = int(pvpDelay) + int(pvpTime)
                if delais > time:
                    p.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "delais_pvp").replace("[[delais]]", iniConfig.GetSettin("config","pvpTime")))
                    return
                else:
                    DataStore.Remove("TeleportPVP", str(player.GameID))
            if iniConfig.GetSetting("config","delayBefore") != str(0):
                ConnectionData = Plugin.CreateDict()
                ConnectionData["Player"] = playerFrom
                ConnectionData["X"] = loc[0]
                ConnectionData["Y"] = loc[1]
                ConnectionData["Z"] = loc[2]
                ConnectionData["Message"] = playerFrom.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "teleport_to_home_delay").replace("[[home]]", quotedargs[0]).replace("[[delay]]", iniConfig.GetSetting("config","delayBefore")))
                Plugin.CreateParallelTimer("Teleport", iniConfig.GetSetting("config","delayBefore")*1000, ConnectionData).Start()
            else:
                playerFrom.GroundTeleport(float(loc[0]), float(loc[1]), float(loc[2]))
                playerFrom.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "teleport_to_home").replace("[[home]]", quotedargs[0]))
        else:
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "home_not_activate"))

    def cmdTp(self, args, player):
        if iniConfig.GetSetting("config", "tp") == str(1):
            quotedargs = Util.GetQuotedArgs(args)
            gid = str(player.GameID)
            time = Plugin.GetTimestamp()
            nombreMax = iniConfig.GetSetting("config", "nb")
            delaisMax = float(iniConfig.GetSetting("config", "delais")) * 1000
            delais = int(delaisTeleport(gid)) + int(delaisMax)
            nombre = nbTeleport(gid)
            if nombre == nombreMax:
                player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "max_tp").replace("[[nb]]", nombreMax))
                return
            if delais > time:
                player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "delais_tp").replace("[[delais]]", iniConfig.GetSetting("config", "delais")))
                return
            if DataStore.ContainsKey("TeleportPVP", str(gid)):
                pvpDelay = DataStore.ContainsKey("TeleportPVP", str(gid))
                pvpTime = int(iniConfig.GetSettin("config","pvpTime")) * 1000
                delais = int(pvpDelay) + int(pvpTime)
                if delais > time:
                    player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "delais_pvp").replace("[[delais]]", iniConfig.GetSettin("config","pvpTime")))
                    p.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "delais_pvp").replace("[[delais]]", iniConfig.GetSettin("config","pvpTime")))
                    return
                else:
                    DataStore.Remove("TeleportPVP", str(gid))
            p = self.CheckV(Player, args)
            if DataStore.ContainsKey("TeleportPVP", str(p.GameID)):
                pvpDelay = DataStore.ContainsKey("TeleportPVP", str(p.GameID))
                pvpTime = int(iniConfig.GetSettin("config","pvpTime")) * 1000
                delais = int(pvpDelay) + int(pvpTime)
                if delais > time:
                    player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "delais_pvp").replace("[[delais]]", iniConfig.GetSettin("config","pvpTime")))
                    p.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "delais_pvp").replace("[[delais]]", iniConfig.GetSettin("config","pvpTime")))
                    return
                else:
                    DataStore.Remove("TeleportPVP", str(p.GameID))
            if removePlugin is not None:
                loc = {}
                loc[0] = p.X
                loc[1] = p.Y
                loc[2] = p.Z
                r = remove.Invoke("searchBuilding", loc, str(p.GameID), iniConfig.GetSetting("config", "rad"))
                if r is not None and r == False:
                    p.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "anti_tp_raid"))
                    player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "anti_tp_raid"))
            if str(p.GameID) == str(player.GameID):
                player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "no_tp_yourself"))
                player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "anti_tp_raid"))
                return
            if p is not None:
                if teleportRequest.has_key(str(player.GameID)):
                    teleportRequest[str(player.GameID)][str(p.GameID)] = 1
                else:
                    teleportRequest[str(player.GameID)] = {}
                    teleportRequest[str(player.GameID)][str(p.GameID)] = 1
                p.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "tp_requete").replace("[[name]]", player.Name))
                if iniConfig.GetSetting("config","tpRequestDelay") != str(0):
                    ConnectionData = Plugin.CreateDict()
                    ConnectionData["PlayerA"] = str(player.GameID)
                    ConnectionData["PlayerB"] = str(p.GameID)
                    Plugin.CreateParallelTimer("TeleportRequest", iniConfig.GetSetting("config","tpRequestDelay")*1000, ConnectionData).Start()
        else:
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "tp_not_activate"))

    def cmdTpAccept(self, args, player):
        if iniConfig.GetSetting("config", "tp") == str(1):
            quotedargs = Util.GetQuotedArgs(args)
            gid = str(player.GameID)
            time = Plugin.GetTimestamp()
            nombreMax = iniConfig.GetSetting("config", "nb")
            delaisMax = float(iniConfig.GetSetting("config", "delais")) * 1000
            p = self.CheckV(Player, args)
            if p is not None:
                if str(p.GameID) == None:
                    player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "player_not_found").replace('[[user]]', quotedargs[0]))
                    return
                if teleportRequest.has_key(str(p.GameID)):
                    t = teleportRequest[str(p.GameID)]
                    if t.has_key(str(gid)) == False:
                        player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "no_tp_request_found"))
                        return
                else:
                    player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "no_tp_request_found"))
                    return
                delais = int(delaisTeleport(str(p.GameID))) + int(delaisMax)
                nombre = nbTeleport(str(p.GameID))
                if nombre == nombreMax:
                    p.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "max_tp").replace("[[nb]]", nombreMax))
                    del teleportRequest[str(p.GameID)]
                    return
                if delais > time:
                    p.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "delais_tp").replace("[[delais]]", iniConfig.GetSetting("config", "delais")))
                    del teleportRequest[str(p.GameID)]
                    return
                if DataStore.ContainsKey("TeleportPVP", gid):
                    pvpDelay = DataStore.ContainsKey("TeleportPVP", gid)
                    pvpTime = int(iniConfig.GetSettin("config","pvpTime")) * 1000
                    delais = int(pvpDelay) + int(pvpTime)
                    if delais > time:
                        player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "delais_pvp").replace("[[delais]]", iniConfig.GetSettin("config","pvpTime")))
                        p.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "delais_pvp").replace("[[delais]]", iniConfig.GetSettin("config","pvpTime")))
                        del teleportRequest[str(p.GameID)]
                        return
                    else:
                        DataStore.Remove("TeleportPVP", str(gid))
                if DataStore.ContainsKey("TeleportPVP", str(p.GameID)):
                    pvpDelay = DataStore.ContainsKey("TeleportPVP", str(p.GameID))
                    pvpTime = int(iniConfig.GetSettin("config","pvpTime")) * 1000
                    delais = int(pvpDelay) + int(pvpTime)
                    if delais > time:
                        player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "delais_pvp").replace("[[delais]]", iniConfig.GetSettin("config","pvpTime")))
                        p.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "delais_pvp").replace("[[delais]]", iniConfig.GetSettin("config","pvpTime")))
                        del teleportRequest[str(p.GameID)]
                        return
                    else:
                        DataStore.Remove("TeleportPVP", str(p.GameID))
                if removePlugin is not None:
                    loc = {}
                    loc[0] = player.X
                    loc[1] = player.Y
                    loc[2] = player.Z
                    r = remove.Invoke("searchBuilding", loc, gid, iniConfig.GetSetting("config", "rad"))
                    if r is not None and r == False:
                        p.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "anti_tp_raid"))
                        player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "anti_tp_raid"))
                if iniConfig.GetSetting("config","delayBefore") != str(0):
                    ConnectionData = Plugin.CreateDict()
                    ConnectionData["Player"] = p
                    ConnectionData["X"] = player.X
                    ConnectionData["Y"] = player.Y
                    ConnectionData["Z"] = player.Z
                    ConnectionData["Message"] = p.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "teleport_to_delay").replace("[[user]]", player.Name).replace("[[delay]]", iniConfig.GetSetting("config","delayBefore")))
                    Plugin.CreateParallelTimer("Teleport", iniConfig.GetSetting("config","delayBefore")*1000, ConnectionData).Start()
                else:
                    p.GroundTeleport(float(player.X), float(player.y), float(player.z))
                    p.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "teleport_to").replace("[[user]]", player.Name))
        else:
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "tp_not_activate"))

    def cmdTpRefuse(self, args, player):
        if iniConfig.GetSetting("config", "tp") == str(1):
            gid = str(player.GameID)
            p = self.CheckV(Player, args)
            if p is not None:
                if str(p.GameID) == None:
                    player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "player_not_found").replace('[[user]]', quotedargs[0]))
                    return
                if teleportRequest.has_key(str(p.GameID)):
                    t = teleportRequest[str(p.GameID)]
                    if t.has_key(str(gid)):
                        p.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "teleport_no_accept").replace("[[user]]", player.Name))
                        del teleportRequest[str(p.GameID)][str(gid)]
                        return
        else:
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "tp_not_activate"))

    def cmdTpList(self, args, player):
        if iniConfig.GetSetting("config", "tp") == str(1):
            gid = str(player.GameID)
            playerFrom.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "teleport_list_request"))
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
        else:
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "tp_not_activate"))

    def cmdAdminTp(self, args, player):
        gid = str(player.GameID)
        if not player.Admin:
            return
        p = self.CheckV(Player, args)
        if p is not None:
            player.GroundTeleport(p.X, p.Y, p.Z)
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "teleport_to_").replace("[[user]]", quotedargs[0]))
            p.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "admin_teleport").replace("[[user]]", player.Name))
            return
        p = self.CheckVSleeping(Player, args)
        if p is not None:
            if(p.Name.lower() == cmd.quotedArgs[0].lower()):
                player.GroundTeleport(p.X, p.Y, p.Z)
                player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "teleport_to_").replace("[[user]]", quotedargs[0]))
                return
        player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "player_not_found").replace('[[user]]', quotedargs[0]))

    def cmdAdminTpLoc(self, args, player):
        player.GroundTeleport(float(quotedargs[0]), float(quotedargs[1]), float(quotedargs[2]))
        player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "teleport_to_pos").replace("[[loc]]", "X=" + str(quotedargs[0]) + " Y=" + str(quotedargs[1]) + " Z=" + str(quotedargs[2])))

    """
        CheckV method based on Spock's method.
        Upgraded by DreTaX
        Can Handle Single argument and Array args.
        V4.0
    """
    def CheckV(self, Player, args):
        ini = self.TpFriendConfig()
        count = 0
        if hasattr(args, '__len__') and (not isinstance(args, str)):
            p = self.GetPlayerName(String.Join(" ", args))
            if p is not None:
                return p
            for pl in Server.ActivePlayers:
                for namePart in args:
                    if namePart.lower() in pl.Name.lower():
                        p = pl
                        count += 1
                        continue
        else:
            p = self.GetPlayerName(str(args))
            if p is not None:
                return p
            for pl in Server.ActivePlayers:
                if str(args).lower() in pl.Name.lower():
                    p = pl
                    count += 1
                    continue
        if count == 0:
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "player_not_found").replace('[[user]]', String.Join(" ", args)))
            return None
        elif count == 1 and p is not None:
            return p
        else:
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "player_similar").replace('[[nb]]', str(count)))
            return None

    """
        CheckV method based on Spock's method.
        Upgraded by DreTaX and M0rdreck
        Can Handle Single argument and Array args.
        V4.0
    """
    def CheckVSleeping(self, Player, args):
        ini = self.TpFriendConfig()
        count = 0
        if hasattr(args, '__len__') and (not isinstance(args, str)):
            p = self.GetPlayerName(String.Join(" ", args))
            if p is not None:
                return p
            for pl in Server.SleepingPlayers:
                for namePart in args:
                    if namePart.lower() in pl.Name.lower():
                        p = pl
                        count += 1
                        continue
        else:
            p = self.GetPlayerName(str(args))
            if p is not None:
                return p
            for pl in Server.SleepingPlayers:
                if str(args).lower() in pl.Name.lower():
                    p = pl
                    count += 1
                    continue
        if count == 0:
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "player_not_found").replace('[[user]]', String.Join(" ", args)))
            return None
        elif count == 1 and p is not None:
            return p
        else:
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("config", "language"), "player_similar").replace('[[nb]]', str(count)))
            return None
